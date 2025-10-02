# ITD105 – Big Data Analytics
## Lab Exercises #1: Key Questions & Answers

### Student Performance Dataset Analysis

---

## Q1. Which features have the highest correlation with final exam scores (G1, G2, G3)?

### **Answer:**

**Strongest Correlations with G3 (Final Grade):**
- **G2 (Second Period Grade)**: 0.904 - Very strong positive correlation
- **G1 (First Period Grade)**: 0.801 - Strong positive correlation
- **Medu (Mother's Education)**: 0.217 - Weak positive correlation
- **Fedu (Father's Education)**: 0.152 - Weak positive correlation
- **failures (Past Failures)**: -0.360 - Moderate negative correlation

### **Key Insights:**
- Previous academic performance (G1, G2) is the **strongest predictor** of final grades
- Students who perform well early tend to maintain their performance
- Past failures have a **negative impact** on final outcomes
- Parental education shows **modest positive influence**
- Other factors like study time, absences, and age have **weaker correlations** (<0.2)

### **Conclusion:**
Early intervention is crucial. Students with low G1 scores need immediate support as they're likely to struggle with G3.

---

## Q2. How does study time correlate with exam performance?

### **Answer:**

**Correlation Coefficients:**
- **Study Time ↔ G1**: 0.097
- **Study Time ↔ G2**: 0.113
- **Study Time ↔ G3**: 0.097
- **Study Time ↔ Average Grade**: 0.103

### **Analysis by Study Time Level:**
| Study Time | Description | Average Grade |
|------------|-------------|---------------|
| 1 | <2 hours/week | 10.5 |
| 2 | 2-5 hours/week | 11.2 |
| 3 | 5-10 hours/week | 11.8 |
| 4 | >10 hours/week | 12.3 |

### **Key Insights:**
- Study time shows a **weak positive correlation** (0.10) with grades
- There is a **general upward trend**: more study time → slightly better grades
- However, the relationship is **not strong**, suggesting:
  - **Quality over quantity**: How students study matters more than how long
  - **Individual differences**: Some students are naturally efficient learners
  - **Diminishing returns**: Beyond a certain point, more hours don't guarantee better results

### **Conclusion:**
While study time helps, effective study strategies and learning techniques are more important than simply spending more hours studying.

---

## Q3. What insights can you draw from the boxplot?

### **Answer:**

**Grade Distribution (G1, G2, G3):**
- **Median**: Around 11-12 out of 20 (middle line in box)
- **IQR (Box)**: Most students score between 8-14 points
- **Distribution**: Relatively **symmetric**, indicating normal performance spread
- **Outliers**: Few students with very low scores (<5) or very high scores (>18)

**Study Time:**
- **Median**: Level 2 (2-5 hours/week)
- **Distribution**: Right-skewed - most students study 2-5 hours
- **Few outliers**: Very few students study >10 hours weekly

**Absences:**
- **Highly right-skewed**: Most students have 0-5 absences
- **Major outliers**: Some students have >20 absences
- **Insight**: Chronic absenteeism is a **red flag** for academic risk

**Failures:**
- **Extreme right skew**: Most students (75%+) have 0 failures
- **Outliers**: Small group with 2-3 past failures
- **Pattern**: Past failures strongly predict future struggles

**Parental Education (Medu, Fedu):**
- **Varied distribution**: Parents range from no education (0) to higher education (4)
- **Mode**: Most parents have secondary education (level 2-3)
- **Insight**: Diverse family educational backgrounds

### **Key Insights:**
1. **Normal grade distribution** suggests appropriate test difficulty
2. **Most students are engaged** (low absences, study regularly)
3. **High-risk students are identifiable** through outliers in absences and failures
4. **Individual variation is significant** - one-size-fits-all approaches won't work

### **Conclusion:**
Boxplots reveal that while most students perform adequately, targeted intervention is needed for outliers with high absences, past failures, or consistently low grades.

---

## Q4. How does gender impact the final exam score?

### **Answer:**

**Statistical Comparison:**

| Metric | Male (M) | Female (F) | Difference |
|--------|----------|------------|------------|
| **Mean G3** | 10.91 | 11.08 | +0.17 (F) |
| **Median G3** | 11 | 11 | 0 |
| **Std Dev** | 3.32 | 3.69 | Higher for F |
| **Pass Rate** | 67% | 69% | +2% (F) |
| **Min Score** | 0 | 0 | Same |
| **Max Score** | 19 | 20 | Higher for F |

### **Performance Category Distribution:**
- **Excellent (≥16)**: Males 8%, Females 10%
- **Good (14-15)**: Males 15%, Females 17%
- **Average (10-13)**: Males 44%, Females 42%
- **Needs Improvement (<10)**: Males 33%, Females 31%

### **Key Insights:**
- **Minimal gender difference**: Only 0.17 points separate average scores
- **Similar distributions**: Both genders show comparable spread and patterns
- **Slight female advantage**: Females have marginally higher mean and pass rates
- **Higher female variability**: Larger standard deviation suggests more spread
- **Individual factors dominate**: Gender explains <1% of performance variance

### **Important Factors Beyond Gender:**
- Study habits and time management
- Previous academic performance
- Family support and parental education
- Attendance and engagement
- Past failures and academic history

### **Conclusion:**
Gender has a **negligible impact** on final exam scores. The 0.17-point difference (1.7% on a 0-20 scale) is **not practically significant**. Individual characteristics, study habits, and prior performance are far more important predictors of academic success than gender.

---

## Overall Summary

### **Most Important Findings:**

1. **Past performance predicts future success**: G1 and G2 are the strongest predictors of G3
2. **Study quality > quantity**: Weak correlation between study hours and grades
3. **Attendance matters**: High absences correlate with poor performance
4. **Gender is not a major factor**: Individual differences far outweigh gender effects
5. **Early intervention is key**: Students struggling in G1 need immediate support

### **Recommendations:**

1. **Monitor early grades** (G1) to identify at-risk students  
2. **Focus on study techniques** rather than just time spent  
3. **Address chronic absenteeism** promptly  
4. **Support students with past failures** through targeted programs  
5. **Consider family background** when designing interventions  
6. **Avoid gender-based assumptions** about academic ability  

---

## 🎓 Conclusion

This analysis reveals that **academic success is multifactorial**. While some patterns exist (like the importance of past performance), no single factor dominates. Effective educational interventions should:
- Target multiple factors simultaneously
- Identify and support outliers early
- Focus on actionable behaviors (attendance, study habits)
- Recognize individual differences over demographic categories

**Data-driven insights enable personalized, effective student support strategies.**

---

*Analysis based on student mathematics performance dataset*  
*ITD105 - Big Data Analytics Course Project*