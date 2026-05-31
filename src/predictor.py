import pandas as pd
import os
import warnings
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

warnings.filterwarnings('ignore')

# 1. Define Data Paths
DATA_DIR = r"C:\Users\chinm\OneDrive\Desktop\Student_Performance_Analysis\data"

info_df = pd.read_csv(os.path.join(DATA_DIR, 'studentInfo.csv'))
registration_df = pd.read_csv(os.path.join(DATA_DIR, 'studentRegistration.csv'))
assessments_df = pd.read_csv(os.path.join(DATA_DIR, 'assessments.csv'))
student_assessments_df = pd.read_csv(os.path.join(DATA_DIR, 'studentAssessment.csv'))
materials_df = pd.read_csv(os.path.join(DATA_DIR, 'vle.csv'))

# 2. Registration Features
reg_features = registration_df[['id_student','code_module','code_presentation','date_registration']].copy()
reg_features['date_registration'] = reg_features['date_registration'].fillna(reg_features['date_registration'].median())

# 3. Assessment Features
merged_assessments = pd.merge(student_assessments_df, assessments_df, on='id_assessment', how='left')

# First assessment score
first_assessments = merged_assessments.sort_values('date_submitted').groupby(
    ['id_student','code_module','code_presentation']).first().reset_index()
score_features = first_assessments[['id_student','code_module','code_presentation','score']].copy()
score_features.rename(columns={'score':'first_assessment_score'}, inplace=True)

# Last assessment score (for improvement trend)
last_assessments = merged_assessments.sort_values('date_submitted').groupby(
    ['id_student','code_module','code_presentation']).last().reset_index()
last_scores = last_assessments[['id_student','code_module','code_presentation','score']].copy()
last_scores.rename(columns={'score':'last_assessment_score'}, inplace=True)

# Weighted average score
merged_assessments['weighted_score'] = merged_assessments['score'] * merged_assessments['weight'] / 100
weighted_scores = merged_assessments.groupby(['id_student','code_module','code_presentation'])['weighted_score'].mean().reset_index()
weighted_scores.rename(columns={'weighted_score':'weighted_avg_score'}, inplace=True)

# 4. Early Engagement (first 4 weeks)
chunk_size = 500000
early_clicks_list = []
for chunk in pd.read_csv(os.path.join(DATA_DIR, 'studentVle.csv'), chunksize=chunk_size):
    early_chunk = chunk[chunk['date'] <= 28].copy()
    early_chunk['week'] = pd.cut(early_chunk['date'], bins=[-1, 7, 14, 21, 28], labels=['wk1','wk2','wk3','wk4'])
    early_clicks_list.append(early_chunk)
early_clicks = pd.concat(early_clicks_list, ignore_index=True)

# 5. Behavioral Profiling
early_clicks_detailed = early_clicks.merge(materials_df[['id_site','activity_type']], on='id_site', how='left')
click_features = early_clicks_detailed.pivot_table(
    index=['id_student','code_module','code_presentation'],
    columns='activity_type',
    values='sum_click',
    aggfunc='sum',
    fill_value=0
).reset_index()

activity_cols = click_features.columns.drop(['id_student','code_module','code_presentation'])
click_features['total_early_clicks'] = click_features[activity_cols].sum(axis=1)
click_features['activity_diversity'] = (click_features[activity_cols] > 0).sum(axis=1)

weekly_clicks = early_clicks.pivot_table(
    index=['id_student','code_module','code_presentation'],
    columns='week',
    values='sum_click',
    aggfunc='sum',
    fill_value=0
).reset_index()
weekly_clicks['momentum_trend'] = weekly_clicks['wk4'] - weekly_clicks['wk1']
weekly_clicks['dropoff_ratio'] = (weekly_clicks['wk1'] + weekly_clicks['wk2']) / (weekly_clicks['wk3'] + weekly_clicks['wk4'] + 1)

click_features = pd.merge(click_features, weekly_clicks, on=['id_student','code_module','code_presentation'], how='left')

# 6. Merge Feature Space
df = pd.merge(info_df, click_features, on=['id_student','code_module','code_presentation'], how='left')
df = pd.merge(df, reg_features, on=['id_student','code_module','code_presentation'], how='left')
df = pd.merge(df, score_features, on=['id_student','code_module','code_presentation'], how='left')
df = pd.merge(df, last_scores, on=['id_student','code_module','code_presentation'], how='left')
df = pd.merge(df, weighted_scores, on=['id_student','code_module','code_presentation'], how='left')

# Improvement trend
df['score_improvement'] = df['last_assessment_score'].fillna(0) - df['first_assessment_score'].fillna(0)

fill_zero_cols = list(activity_cols) + ['total_early_clicks','activity_diversity','wk1','wk2','wk3','wk4',
                                       'momentum_trend','dropoff_ratio','first_assessment_score',
                                       'last_assessment_score','weighted_avg_score','score_improvement']
for col in fill_zero_cols:
    df[col] = df[col].fillna(0)

# 7. Target Transformation
df['final_result'] = df['final_result'].astype(str).str.strip()
risk_mapping = {'Distinction':0,'Pass':0,'Fail':1,'Withdrawn':1}
df['risk_label'] = df['final_result'].map(risk_mapping)
df = df.dropna(subset=['risk_label']).copy()
df['risk_label'] = df['risk_label'].astype(int)

# 8. Features
features = ['num_of_prev_attempts','studied_credits','date_registration',
            'first_assessment_score','last_assessment_score','score_improvement',
            'weighted_avg_score','total_early_clicks','activity_diversity',
            'wk1','wk2','wk3','wk4','momentum_trend','dropoff_ratio'] + list(activity_cols)

X = pd.get_dummies(df[features])
y = df['risk_label']

# 9. Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42,stratify=y)

risk_count = (y_train==1).sum()
safe_count = (y_train==0).sum()
scale_weight = safe_count / risk_count

# 10. Train XGBoost
model = xgb.XGBClassifier(
    n_estimators=800,
    max_depth=6,
    learning_rate=0.04,
    subsample=0.9,
    colsample_bytree=0.9,
    scale_pos_weight=scale_weight,
    random_state=42,
    eval_metric='logloss'
)

model.fit(X_train,y_train,verbose=False)

# 11. Evaluate
y_pred = model.predict(X_test)
acc = accuracy_score(y_test,y_pred)
print(f"-> Enhanced Model Accuracy: {acc:.2%}")

# 12. Export Predictions
# 12. Export Predictions with Custom Risk Logic
df['Predicted_Risk_Status'] = model.predict(X)

# Map initial AI prediction
df['Predicted_Risk_Status'] = df['Predicted_Risk_Status'].map({0: 'Safe', 1: 'At Risk'})

# Apply custom logic
def custom_risk(row):
    if row['Predicted_Risk_Status'] == 'At Risk':
        return 'High Risk'
    elif row['Predicted_Risk_Status'] == 'Safe' and row['momentum_trend'] < 0:
        return 'Monitor'
    elif row['Predicted_Risk_Status'] == 'Safe' and row['momentum_trend'] >= 0:
        return 'Safe'
    else:
        return 'Unknown'

df['Predicted_Risk_Status'] = df.apply(custom_risk, axis=1)

# Map actual labels for comparison
df['risk_label'] = df['risk_label'].map({0: 'Safe', 1: 'At Risk'})

export_cols = [
    'id_student', 'code_module', 'code_presentation', 'final_result', 'risk_label',
    'Predicted_Risk_Status', 'date_registration', 'first_assessment_score',
    'last_assessment_score', 'score_improvement', 'weighted_avg_score',
    'total_early_clicks', 'activity_diversity', 'momentum_trend', 'dropoff_ratio'
] + list(activity_cols)

final_export = df[export_cols]
final_export.to_csv('ML_Predicted_Early_Warning_Data.csv', index=False)
print("\nSUCCESS! Predictions saved to 'ML_Predicted_Early_Warning_Data.csv'")
