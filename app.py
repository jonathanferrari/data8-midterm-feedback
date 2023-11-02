import streamlit as st
import pandas as pd
import numpy as np

categories = ["GSI", "AI", "Lab", "Ed", "Office Hours", "Lecture", "Resources"]

class Analyze:
    """
    Class to contain all the analysis functions for each of the topics in the dataset
    """
    column_categories = {
        "Resources": [1, 28],
        "Office Hours": list(range(2, 24)),
        "Lecture" : [24, 25, 26, 27, 29],
        "Ed" : list(range(30, 44)),
        "Lab" : list(range(44, 51)) + [69],
        "GSI" : list(range(53, 65)),
        "AI" : list(range(65, 69))
    }
    
    def __init__(self, df):
        self.df = df
        self.data = {k : df.iloc[:, v] for k, v in self.column_categories.items()}
        self.data["All"] = df.iloc[:, 1:]
    
    def get(self, topic):
        """
        Get the data for a particular topic
        """
        return self.data[topic]
    
    def gsi_analyze(self):
        df = self.get("GSI")
        names = ["Name", "Worksheet Pacing", "Overall", 
                "Preparedness", "Section Pacing",
                "Clarity", "Approachability",
                "Atmosphere", "Promotes Discussion",
                "Email Responsiveness", 
                "Does Well", "Could Improve"]
        gsi_name = df.iloc[0, 0]
        df.columns = names
        df = df.replace({"Needs Improvement" : 0, "Average" : 1/2, "Excellent" : 1})
        df["Overall"] = df["Overall"]/5
        df["Worksheet Pacing"] = df["Worksheet Pacing"] == 2
        nums = (pd.concat([df.mean(numeric_only=True), 
                          df.std(numeric_only=True)], axis=1)
                .rename(columns={0 : "mean", 1 : "std"})
                .T
                .to_dict())
        results = {"numbers" : nums , "name" : gsi_name,
                "feedback" : {"good" : df["Does Well"].dropna(), "bad" : df["Could Improve"].dropna()}}
        return results
    
    def gsi_display(self):
        results = self.gsi_analyze()
        st.subheader("GSI Name:", divider="grey")
        st.write(results["name"])
        st.subheader("Does Well:", divider="rainbow")
        for i in results["feedback"]["good"]:
            st.markdown(f"- {i}")
        st.subheader("Could Improve:", divider="rainbow")
        for i in results["feedback"]["bad"]:
            st.markdown(f"- {i}")
        for k, v in results["numbers"].items():
            st.subheader(k, divider="rainbow")
            st.latex(f"\\text{{Mean}}: {round(v['mean'], 3)} \\newline \\text{{Standard Deviation}}: {round(v['std'], 3)}")
    
    def ai_analyze(self):
        df = self.get("AI")
        names = ["Approachability", "Helpfulness", "Clarity", "Improvement"]
        df.columns = names
        df = df.replace({"Needs Improvement" : 0, "Average" : 1/2, "Excellent" : 1})
        nums = (pd.concat([df.mean(numeric_only=True), 
                            df.std(numeric_only=True)], axis=1)
                    .rename(columns={0 : "mean", 1 : "std"})
                    .T
                    .to_dict())
        results = {"numbers" : nums ,
                    "feedback" : list(df.Improvement.dropna())}
        return results
    
    def ai_display(self):
        results = self.ai_analyze()
        st.subheader("Could Improve:", divider="rainbow")
        for i in results["feedback"]:
            st.markdown(f"- {i}")
        for k, v in results["numbers"].items():
            st.subheader(k, divider="rainbow")
            st.latex(f"\\text{{Mean}}: {round(v['mean'], 3)} \\newline \\text{{Standard Deviation}}: {round(v['std'], 3)}")
            
    def lab_analyze(self):
        df = self.get("Lab")
        names = ["Worksheet Helpfulness", "Worksheet Length", "Worksheet Difficulty", 
                "Notebook Helpfulness", "Notebook Length", "Notebook Difficulty",
                "Minutes Spent on Notebook Outside of Lab", "Comments"]
        df.columns = names
        df = df.replace({
                "No time outside of lab" : 0,
                "0 - 30 minutes": 15,
                "30 minutes - 1 hour": 45,
                "1 hour - 1.5 hours": 75,
                "1.5 hours - 2 hours": 105,
                "2+ hours": 135,
            })
        for col in df.columns[:6]:
            df[col] = df[col]/5
        nums = (pd.concat([df.mean(numeric_only=True),
                            df.std(numeric_only=True)], axis=1)
                    .rename(columns={0 : "mean", 1 : "std"})
                    .T
                    .to_dict())
        results = {"numbers" : nums , "feedback" : list(df.Comments.dropna())}
        return results
    
    def lab_display(self):
        results = self.lab_analyze()
        st.subheader("Comments:", divider="rainbow")
        for i in results["feedback"]:
            st.markdown(f"- {i}")
        for k, v in results["numbers"].items():
            st.subheader(k, divider="rainbow")
            st.latex(f"\\text{{Mean}}: {round(v['mean'], 3)} \\newline \\text{{Standard Deviation}}: {round(v['std'], 3)}")
    
    def ed_analyze(self):
        df = self.get("Ed")
        names = ["Post Frequency", "How Can We Improve", 
                "Homework Use", "Lab Use", "Project Use", "Discussion Use", "Lecture Use",
                "Clarity", "Attitude", "Response Time", "Experienced", "Elaborate", "Other Feedback", "Quality"
                ]
        df.columns = names
        improvement = df["How Can We Improve"].dropna()
        other_feedback = df["Other Feedback"].dropna()
        experienced = df["Experienced"][df["Experienced"] != "None of the above."].apply(lambda x: x.split(",")).explode().value_counts().to_dict()
        elaborate = df["Elaborate"].dropna()
        df = (df
            .drop(columns=["How Can We Improve", "Other Feedback", "Experienced", "Elaborate", "Post Frequency"])
            .replace({
                "5 (Least common/Never)" : 5,
                "1 (Most common)" : 1,
                "Excellent" : 1,
                "Good" : 1/2,
                "Poor" : 0,
            }))
        df["Quality"] = df["Quality"]/5
        for col in df.columns[:5]:
            df[col] = (6-df[col].astype(float))/5
        nums = (pd.concat([df.mean(numeric_only=True),
                                df.std(numeric_only=True)], axis=1)
                        .rename(columns={0 : "mean", 1 : "std"})
                        .T
                        .to_dict())
        results = {
            "numbers" : nums,
            "feedback" :
                {
                    "improvement" : improvement,
                    "other_feedback" : other_feedback,
                    "experienced" : experienced,
                    "elaborate" : elaborate
                }
        }
        return results
    
    def ed_display(self):
        results = self.ed_analyze()
        st.subheader("How Can We Improve:", divider="rainbow")
        for i in results["feedback"]["improvement"]:
            st.markdown(f"- {i}")
        st.subheader("Other Feedback:", divider="rainbow")
        for i in results["feedback"]["other_feedback"]:
            st.markdown(f"- {i}")
        st.subheader("Experienced:", divider="rainbow")
        for k, v in results["feedback"]["experienced"].items():
            st.markdown(f"- {k} (${v}$)")
        st.subheader("Elaborate:", divider="rainbow")
        for i in results["feedback"]["elaborate"]:
            st.markdown(f"- {i}")
        for k, v in results["numbers"].items():
            st.subheader(k, divider="rainbow")
            st.latex(f"\\text{{Mean}}: {round(v['mean'], 3)} \\newline \\text{{Standard Deviation}}: {round(v['std'], 3)}")
    
    def resources_analyze(self):
        df = self.get("Resources")
        names = ["What resources are you aware of?", "How Helpful is the textbook?"]
        df.columns = names
        df.iloc[:, 1] = df.iloc[:, 1].dropna()/5
        nums = (pd.concat([df.mean(numeric_only=True),
                        df.std(numeric_only=True)], axis=1)
                            .rename(columns={0 : "mean", 1 : "std"})
                            .T
                            .to_dict())
        resources = df["What resources are you aware of?"].dropna().apply(lambda x: x.split(",")).explode().value_counts().to_dict()
        results = {"numbers" : nums, "resources" : resources,}
        return results

    def resources_display(self):
        results = self.resources_analyze()
        tb_label = "How Helpful is the textbook?"
        st.subheader("What resources are you aware of?", divider="rainbow")
        for k, v in results["resources"].items():
            st.markdown(f"- {k} (${v}$)")
        st.subheader(tb_label, divider="rainbow")
        st.latex(f"\\text{{Mean}}: {round(results['numbers'][tb_label]['mean'], 3)} \\newline \\text{{Standard Deviation}}: {round(results['numbers'][tb_label]['std'], 3)}")
    
    def lecture_analyze(self):
        df = self.get("Lecture")
        names = ["Absorb Lecture", "Helfpulness", "Pacing", "Composition (0=all slides, 5=all demo)", "Comments"]
        df.columns = names
        comments = list(df["Comments"].dropna())
        absorb = df["Absorb Lecture"].dropna().apply(lambda x: x.split(",")).explode().value_counts().to_dict()
        df = df.drop(columns=["Comments", "Absorb Lecture"])
        for col in df.columns:
            df[col] = df[col]/5
        nums = (pd.concat([df.mean(numeric_only=True),
                        df.std(numeric_only=True)], axis=1)
                        .rename(columns={0 : "mean", 1 : "std"})
                        .T
                        .to_dict())
        results = {
            "numbers" : nums,
            "feedback" :
                {
                    "comments" : comments,
                    "absorb" : absorb,
                }
        }
        return results
    
    def lecture_display(self):
        results = self.lecture_analyze()
        st.subheader("Comments:", divider="rainbow")
        for i in results["feedback"]["comments"]:
            st.markdown(f"- {i}")
        st.subheader("How do you absorb lecture?", divider="rainbow")
        for k, v in results["feedback"]["absorb"].items():
            st.markdown(f"- {k} (${v}$)")
        for k, v in results["numbers"].items():
            st.subheader(k, divider="rainbow")
            st.latex(f"\\text{{Mean}}: {round(v['mean'], 3)} \\newline \\text{{Standard Deviation}}: {round(v['std'], 3)}")
        
    def office_hours_analyze(self):
        df = self.get("Office Hours")
        names = ["Attended",
                "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", 
                "Modality", "How Can We Improve",
                "Non-project wait", "Project wait",
                "Homework Use", "Lab Use", "Project Use", "Discussion Use", "Lecture Use",
                "Clarity", "Approachability", "Atmosphere", 
                "Experienced", "Elaborate", "Other Feedback", 
                "Quality"
                    ]
        df.columns = names
        improvement = list(df["How Can We Improve"].dropna())
        other_feedback = list(df["Other Feedback"].dropna())
        experienced = df["Experienced"][df["Experienced"] != "None of the above."].dropna().apply(lambda x: x.split(",")).explode().value_counts().to_dict()
        elaborate = list(df["Elaborate"].dropna())
        mode = df["Modality"].dropna().value_counts().to_dict()
        df = (df
            .drop(columns=["How Can We Improve", "Other Feedback", "Experienced", "Elaborate", "Modality"])
            .drop(columns=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
            .replace({
                "5 (Least common/Never)" : 5,
                "1 (Most common)" : 1,
                "Excellent" : 1,
                "Good" : 1/2,
                "Poor" : 0,
                "Yes" : 1,
                "No" : 0,
                "I have not attended OH during a non-project week" : np.nan,
                "I have not attended OH during a project week" : np.nan,
                "0-15 minutes" : 7.5,
                "15-30 minutes" : 22.5,
                "30-45 minutes" : 37.5,
                "Over 45 minutes" : 52.5,
            }))
        df["Quality"] = df["Quality"]/5
        for col in df.columns[3:8]:
                df[col] = (6-df[col].astype(float))/5
        nums = (pd.concat([df.mean(numeric_only=True),
                        df.std(numeric_only=True)], axis=1)
                        .rename(columns={0 : "mean", 1 : "std"})
                        .T
                        .to_dict())
        feedback = {
            "improvement" : improvement,
            "other_feedback" : other_feedback,
            "experienced" : experienced,
            "elaborate" : elaborate
        }
        results = {"numbers" : nums, "feedback" : feedback, "mode" : mode}
        return results
    
    def office_hours_display(self):
        results = self.office_hours_analyze()
        st.subheader("How Can We Improve:", divider="rainbow")
        for i in results["feedback"]["improvement"]:
            st.markdown(f"- {i}")
        st.subheader("Other Feedback:", divider="rainbow")
        for i in results["feedback"]["other_feedback"]:
            st.markdown(f"- {i}")
        st.subheader("Experienced:", divider="rainbow")
        for k, v in results["feedback"]["experienced"].items():
            st.markdown(f"- {k} (${v}$)")
        st.subheader("Elaborate:", divider="rainbow")
        for i in results["feedback"]["elaborate"]:
            st.markdown(f"- {i}")
        st.subheader("Modality:", divider="rainbow")
        for k, v in results["mode"].items():
            st.markdown(f"- {k} (${v}$)")
        for k, v in results["numbers"].items():
            st.subheader(k, divider="rainbow")
            st.latex(f"\\text{{Mean}}: {round(v['mean'], 3)} \\newline \\text{{Standard Deviation}}: {round(v['std'], 3)}")
    
def load_data(file):
    data = pd.read_csv(file)
    return data

st.title('Data 8 Feedback Analysis App')

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    data = Analyze(load_data(uploaded_file))
    st.write('Data Loaded Successfully!')
    show_data = st.toggle('Show Data', False)
    if show_data:
        st.write(data.df)

    with st.sidebar:
        st.subheader('Select Question Type')
        categories = st.multiselect('Select Question Type', categories)
    for category in categories:
        with st.expander(f"**{category}**", expanded=True):
            eval(f"data.{category.lower().replace(' ', '_')}_display()")

        

