from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

# Sample statistical questions dictionary
statistical_questions={
    0:{
        "stats_question":"Let get started with determining which statistical method is best suited for your data",
        "options": ["Start","Back"],
        "next_question":[1,0]
    },
    #only one variable of intererst
    1:{
        #variable of interest
        "stats_question":"Number Of Variable Of Interest ?",
        "options": ["Only One Variable Of Interest","Two Variables Of Interest","More Than Two Variables Of Interest","Back"],
        "next_question":[2,16,25,0]
    }, 
    2:{
        # type of sample problem
        "stats_question":"Type Of Sample Problem ?",
        "options": ["One Sample Problem","Two Sample Problem","More Than Two Sample Problem","Back"],
        "next_question":[3,7,6,1]
    },
    #distribution type
    3:{
        "stats_question":"Type Of Underlying Distibution ?",
        "options": ["Normal Distribution","Binomial Distibution","Poisson Distribution","None","Back"],
        "next_question":[4,5,"Use One Sample Poisson Test","Use Another Underlying Distribution Or Use Nonparametric Methods",2]
    },
    #inference concerning
    4:{
        "stats_question":"Inference Concerning ?",
        "options":["Inference Concerning known","Inference Concerning not known","No Inference Concerning","Back"],
        "next_question":["Use One sample z-test","Use One sample t-test","Use One sample chi-square test for variances",3]
    },
    #normal appoximation
    5:{
       "stats_question":"Is Normal Approximation Valid ?",
       "options": ["Yes","No","Back"],
       "next_question":["Use Normal-Theory Methods","Use Exact Methods",3]
    },
    #distibution type 1
    7:{
        "stats_question":"Type Of Underlying Distibution ?",
        "options": ["Normal Distribution","Binomial Distibution","Person Time Data","None","Back"],
        "next_question":[8,9,27,"Use Another Underlying Distribution or Use Nonparametric Methods",2]

    },
    #inference concerning 1
    8:{
        "stats_question":"Inference Concerning Means ?",
        "options": ["Yes","No","Back"],
        "next_question":[11,"Use Two Sample F Test To Compare Variances",7]

    },
    #samples independent 1
    9:{
        "stats_question":"Are Samples Independent?",
        "options": ["Yes","No","Back"],
        "next_question":[10,"Use McNemar's Test",7]
    },
    # expected values >=5
    10:{
        "stats_question":"Are All Expected Values >=5 ?",
        "options": ["Yes","No","Back"],
        "next_question":[14,"Use Fisher's Exact Test",9]
    },
    #samples independent 3
    11:{
        "stats_question":"Are Samples Independent ?",
        "options": ["Yes","No","Back"],
        "next_question":[12,"Use Paired T Test",8]
    },
    #variance 3
    12:{
        "stats_question":"Are Variances Of Two Sample Significantlt Different ?\nNote:Test Using F TEST",
        "options": ["Yes","No","Back"],
        "next_question":["Use Two Sample T Test With Unequal Variances","Use Two Sample T Test With equal Variances",11]
    },
    #more than two sample and checking normal distribution 2
    6:{
        "stats_question":"Is Underlying Distribution Normal ?",
        "options": ["Yes","No","Back"],
        "next_question":["USE One Way ANOVA",13,2]
    },
    # caregorical data 2
    13:{
        "stats_question":"Are Data Categorical?",
        "options": ["Yes","No","Back"],
        "next_question":["Use R x C Contingency Table Methods","Use Another Underlying Distribution Or Use Nonparametric Methods Such AS Kruskal Wallis Test",6]
    },
    #contingency table 6
    14:{
        "stats_question":"Contingency Table ?",
        "options": ["2 x 2 Contingency Table","2 x k Contingency Table"," R x C Contingency Table , R>2,C>2","BACK"],
        "next_question":["Use Two Sample Test For Binomial Propotions, Or 2 x 2 Contigency Table Methods If No Confounding Is Present,Or The Mantel Haenszel Test If Cofounding Is Present",15,"Use Chi Square Test For R X C Tables",10]
    },
    # a and b
    15:{
        "stats_question":"Interested In Trend Over K Bionomial Propotions ?",
        "options": ["Yes","No","Back"],
        "next_question":["Use Chi Square Test For Trend, If No Confounding Is Present, Or The Mental Extension Test If Confounding Is Present","Use Chi Square Test For Heterogeneity For 2 x K Tables",14]
    },
    #type of variable for two variables 4
    16:{
        "stats_question":"Variable Types ?",
        "options": ["Both Variables Are Continuous","One Variable Continuous And One Categorical","Both Variables Are Categorical","Ordinal Data","Back"],
        "next_question":[17,19,24,"Use Rank Correlation Methods",1]
    },
    #interested in relationship between two variables 4
    17:{
        "stats_question":"What type of analysis are you interested in conducting between two variables ?",
        "options": ["Interested In Predicting One Variable From Another","Interested In Studying The Correlation Between Two Variables","Back"],
        "next_question":["Use Simple Linear Regression",18,16]
    },
    #normal variables 4
    18:{
        "stats_question":"Are Both Variables Normal ?",
        "options": ["Yes","No","Back"],
        "next_question":["Use Pearson Correlation Methods","Use Rank Correlation Methods",17]
    },
    # number of ways 4
    19:{
        "stats_question":"Number Of Ways In Which The Categorical Variable Can Be Classified ?",
        "options": ["1","2","More Than 2","Back"],
        "next_question":[20,22,23,16 ]

    },
    #normal variable 4
    20:{
        "stats_question":"Is Outcome Variable Normal Or Central Limit Theorem Be Assumed To Hold ?",
        "options": ["Yes","No","Back"],
        "next_question":[21,"Use Kruskal Wallis Test",19]
    },
    #covariates 4
    21:{
        "stats_question":"Other Covariates To Be Controlled For ?",
        "options": ["Yes","No","Back"],
        "next_question":["USE One Way ANCOVA","USE One Way ANOVA",20]
    },
    #other covariates for 2 4
    22:{
        "stats_question":"Other Covariates To Be Controlled For ?",
        "options": ["Yes","No","Back"],
        "next_question":["USE Two Way ANCOVA","USE Two Way ANOVA",19]
    },
    #other covariates for  more than 2 4
    23:{
        "stats_question":"Other Covariates To Be Controlled For ?",
        "options": ["Yes","No","Back"],
        "next_question":["USE Higher Way ANCOVA","USE Higher Way ANOVA",19]
    },
    #test of association 4
    24:{
        "stats_question":"Are You Interested In Tests Of Association Or Reproducibility ?",
        "options": ["Association","Reproducibility","Back"],
        "next_question":["Use Contingency Table Methods","Use Kappa Statistic",16]
    },
    #continuous or binary (more than two variables) 4
    25:{
        "stats_question":"Are Outcome Variables Continuous Or Binary?",
        "options": ["Continuous","Binary","Back"],
        "next_question":["Use Multiple Regression Methods",26,1]
    },
    #binary 4
    26:{
        "stats_question":"Is Time Of Events Important ?",
        "options": ["Yes","No","Back"],
        "next_question":[27,"Use Multiple Logistic Regression Methods",25]
    },
    #one sample problem 5
    27:{
        "stats_question":"One Sample Problem ?",
        "options": ["Yes","No","Back"],
        "next_question":["Use One Sample Test For Incidence Rates",28,26]
    },
    #Incidence Rates Remains Constant Over TIme 5
    28:{
        "stats_question":"Is Incidence Rates Remains Constant Over Time ?",
        "options": ["Yes","No","Back"],
        "next_question":[29,30,27]
    },
    #two sample problem 5
    29:{
        "stats_question":"Two Sample Problem ?",
        "options": ["Yes","No","Back"],
        "next_question":["Use Two Sample Test For Comparision Of Incidence Rates, If No Confounding Is Present; Or Methods For Stratified Person Time Data, If Confounding Is Present","Use Test Of Trend For Incidence Rates",28]
    },
    #Comparision Of Survival Curves Of Two Groups With Limited Control Of Covariates 5
    30:{
        "stats_question":"Interested In Comparision Of Survival Curves Of Two Groups With Limited Control Of Covariates ?",
        "options": ["Yes","No","Back"],
        "next_question":["Use Log Rank Test",31,28]
    },
    #Weibull Distribution 5
    31:{
        "stats_question":"Willing TO Assume Several Curve Comes From A Weibull Distribution ?",
        "options": ["Yes","No","Back"],
        "next_question":["Use Parameter Survival Methods Based On Weibull Distribution","Use Cox Propotional Hazards Model",30]
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/next/<int:question_id>', methods=['GET', 'POST'])
def next_question(question_id):
    question_data = statistical_questions.get(question_id)
    if question_data:
        return jsonify(question_data)
        
        # If it's a POST request, handle user input and return the next question
    next_question_id_or_result = request.json
    if isinstance(next_question_id_or_result, int):
        next_question_id = next_question_id_or_result
        next_question_data = statistical_questions.get(next_question_id)
    else:
        next_question_result = next_question_id_or_result
        return jsonify(next_question_result)  # Return the string result directly

    if next_question_data:
        return jsonify(next_question_data)
    else:
        return jsonify(error="Question not found"), 404
