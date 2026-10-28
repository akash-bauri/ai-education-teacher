# ==========================================
# AI TEACHER ASSISTANT PROMPTS
# ==========================================

DEFAULT_SYSTEM_PROMPT = """
You are an expert NCF 2023 and NEP 2020 aligned AI Teacher Assistant.

PRIMARY ROLE

Your job is to help teachers understand, prepare, teach, assess, and explain educational content.

By default explain content as if you are guiding a teacher who will teach students.

Unless another level is selected:

- Explain at Class 5 level.
- Use simple language.
- Use short sentences.
- Use real-life examples.
- Use classroom-friendly explanations.
- Make concepts easy to teach.

NCF 2023 PRINCIPLES

Always follow:

1. Conceptual Understanding over Rote Learning
2. Competency-Based Learning
3. Activity-Based Learning
4. Inquiry-Based Learning
5. Experiential Learning
6. Inclusive Education
7. Critical Thinking
8. Problem Solving
9. Communication Skills
10. Real-Life Application

Whenever educational content is generated include where appropriate:

- Learning Outcomes
- Competencies
- Activity-Based Learning
- Inclusive Teaching Strategies
- Assessment Suggestions
- Reflection Opportunities

STUDENT LEVEL ADAPTATION

Class 5:
Use simple examples, stories, visuals, activities.

Class 6-8:
Encourage exploration, inquiry, reasoning.

Class 9-10:
Encourage analysis, application, problem solving.

Class 11-12:
Encourage critical thinking, evaluation, interdisciplinary understanding.

INCLUSIVE EDUCATION

Whenever possible provide support for:

- Slow learners
- Visual learners
- Multilingual learners
- Students requiring additional support

OUTPUT STYLE

Always:

- Use headings
- Use bullet points
- Use teacher-friendly language
- Be practical for classroom use

Priority Order:

Understanding > Memorization

Application > Recall

Learning > Marks
"""

# ==========================================
EXPLAIN_TOPIC_PROMPT = """
Explain the following topic in an NCF 2023 aligned way.

Topic:
{topic}

Student Level:
{student_level}

Teaching Style:
{teaching_style}

Generate:

1. Simple Explanation
2. Real-Life Example
3. Learning Outcomes
4. Competencies Developed
5. Activity-Based Learning Idea
6. Inclusive Teaching Tip
7. Quick Assessment Questions

Explain like a teacher preparing for class.

Use simple language.

By default explain at Class 5 level unless another level is selected.
"""

# ==========================================
# NOTES GENERATOR
# ==========================================

NOTES_PROMPT = """
Generate NCF 2023 aligned study notes.

Content:
{content}

Student Level:
{student_level}

Generate:

1. Chapter Overview

2. Learning Outcomes

3. Competencies Developed

4. Key Concepts

5. Detailed Notes

6. Real-Life Examples

7. Activity-Based Learning Suggestion

8. Inclusive Teaching Strategy

9. Quick Revision Points

10. Chapter Summary

Requirements:

- Easy language
- Teacher friendly
- Student friendly
- Revision friendly
- Classroom ready
"""
# ==========================================
# TOPIC NOTES
# ==========================================

TOPIC_NOTES_PROMPT = """
Generate topic-wise NCF aligned notes.

Content:
{content}

For each topic include:

- Topic Name
- Learning Outcomes
- Competencies
- Key Concepts
- Easy Explanation
- Real-Life Example
- Activity Suggestion
- Revision Points

Use teacher-friendly structure.
"""
# ==========================================
# MCQ GENERATOR
# ==========================================

MCQ_PROMPT = """
Generate NCF 2023 aligned MCQs.

Content:
{content}

Student Level:
{student_level}

Generate:

Learning Outcomes

Competencies

Easy Level Questions
(Knowledge & Recall)

Moderate Level Questions
(Understanding & Application)

Hard Level Questions
(Analysis & Evaluation)

Requirements:

- 4 options
- Correct answer
- Explanation
- Competency-based assessment
- Concept-focused questions
- Avoid rote memorization
"""

# ==========================================
# QUESTION PAPER GENERATOR
# ==========================================

QUESTION_PAPER_PROMPT = """
Generate an NCF 2023 aligned question paper.

Content:
{content}

Student Level:
{student_level}

Total Marks:
{marks}

Difficulty:
{difficulty}

Generate:

Learning Outcomes

Competencies

Section A
Easy Questions

Section B
Moderate Questions

Section C
Hard Questions

Section D
Case-Based Questions

Section E
Activity-Based Questions

Include:

- Marks distribution
- Answer key
- Competency mapping
"""

# ==========================================
# LESSON PLAN
# ==========================================

# ==========================================
# LESSON PLAN
# ==========================================

LESSON_PLAN_PROMPT = """
Create a complete NCF 2023 aligned lesson plan.

Topic:
{topic}

Student Level:
{student_level}

Teaching Style:
{teaching_style}

Generate the following sections:

1. Topic Information

- Topic Name
- Class Level
- Duration

2. Learning Outcomes

Describe what students will be able to do after the lesson.

3. Competencies Developed

Examples:
- Critical Thinking
- Problem Solving
- Communication
- Observation
- Collaboration
- Creativity

4. Prior Knowledge

What students should already know.

5. Teaching Learning Materials

Required classroom resources.

6. Activity Based Learning

Include:
- Individual Activity
- Pair Activity
- Group Activity

7. Step-by-Step Teaching Procedure

Teacher Actions:
- Introduction
- Concept Explanation
- Guided Practice
- Activity Facilitation
- Assessment
- Closure

Student Actions:
- Observation
- Discussion
- Participation
- Practice
- Reflection

8. Teacher Explanation Script

Provide a detailed classroom-ready explanation script that the teacher can directly use while teaching.

9. Real-Life Connections

Connect concepts with students' daily life experiences.

10. Inclusive Teaching Strategy

Support:
- Slow learners
- Visual learners
- Auditory learners
- Kinesthetic learners
- Multilingual learners
- Students needing additional support

11. Assessment

Include:
- Oral Questions
- Written Questions
- Higher Order Thinking Questions (HOTS)
- Observation Checklist

12. Reflection

Questions students can reflect upon after the lesson.

13. Homework

Meaningful practice activity aligned with learning outcomes.

Requirements:

- Follow NCF 2023 principles
- Focus on conceptual understanding
- Encourage inquiry-based learning
- Promote experiential learning
- Use simple and student-friendly language
- Make it classroom ready
- Include active participation opportunities
- Explain like an experienced teacher preparing for class
- Use clear headings and structured formatting
"""

# ==========================================
# TEACHING GUIDE
# ==========================================
# ==========================================
# TEACHING GUIDE
# ==========================================

TEACHING_GUIDE_PROMPT = """
Create a complete NCF 2023 aligned teaching guide.

Topic:
{topic}

Student Level:
{student_level}

Teaching Style:
{teaching_style}

Generate the following sections:

1. Chapter Overview

Provide a brief summary of the chapter and its importance.

2. Learning Outcomes

Clearly describe what students will be able to know, understand, and do after completing the lesson.

3. Competencies Developed

Examples:
- Critical Thinking
- Problem Solving
- Communication
- Observation
- Collaboration
- Creativity
- Scientific Temper
- Decision Making

4. Key Concepts

List and explain all important concepts covered in the lesson.

5. Teacher Introduction Script

Provide a detailed classroom-ready introduction script.

Include:
- Greeting
- Attention Grabber
- Prior Knowledge Questions
- Lesson Introduction
- Motivation Strategy

6. Step-by-Step Teaching Strategy

Include:

A. Introduction Phase
- Teacher Actions
- Student Actions

B. Concept Development Phase
- Teacher Explanation
- Student Participation

C. Guided Learning Phase
- Demonstration
- Discussion
- Questioning

D. Practice Phase
- Individual Practice
- Pair Work
- Group Work

E. Assessment Phase
- Quick Checks
- Reflection Questions

F. Closure Phase
- Lesson Summary
- Key Takeaways

7. Real-Life Examples

Provide relatable examples from students' daily lives.

Include:
- Home
- School
- Community
- Environment

8. Activity-Based Learning

Include:

A. Classroom Activities
B. Pair Activities
C. Group Activities
D. Hands-On Activities
E. Inquiry-Based Activities

For each activity provide:
- Objective
- Materials Needed
- Procedure
- Expected Learning

9. Student Engagement Questions

Generate:

- Recall Questions
- Understanding Questions
- Application Questions
- Analysis Questions
- HOTS (Higher Order Thinking Skills) Questions

10. Common Student Misconceptions

For each misconception include:
- Common Mistake
- Why It Happens
- Correction Strategy
- Teacher Tip

11. Inclusive Teaching Strategies

Support:

- Slow Learners
- Advanced Learners
- Visual Learners
- Auditory Learners
- Kinesthetic Learners
- Multilingual Learners
- Students Needing Additional Support

Provide practical classroom adaptations.

12. Assessment Suggestions

Create:

A. Easy Questions
B. Moderate Questions
C. Challenging Questions
D. HOTS Questions

Include:
- Oral Assessment
- Written Assessment
- Activity-Based Assessment

13. Extension Activities

Suggest enrichment tasks for deeper learning.

Examples:
- Projects
- Research Tasks
- Presentations
- Creative Activities

14. Homework Suggestions

Provide meaningful and application-based homework.

Include:
- Practice Work
- Observation Tasks
- Creative Assignments
- Real-Life Application Tasks

15. Lesson Recap

Provide:

- Key Points Summary
- Quick Revision Notes
- Exit Ticket Questions

16. Teacher Reflection Notes

Generate reflection prompts such as:

- What worked well?
- Which concepts were difficult for students?
- How can the lesson be improved?
- What support is needed for struggling learners?

Requirements:

- Follow NCF 2023 principles
- Focus on conceptual understanding
- Encourage experiential learning
- Promote inquiry-based learning
- Support competency-based education
- Use simple and student-friendly language
- Teacher-friendly format
- Practical classroom guidance
- Classroom-ready content
- Include active learning opportunities
- Use clear headings and structured formatting
- Explain like an experienced teacher preparing for a real classroom session
"""


# ==========================================
# HOMEWORK
# ==========================================

# ==========================================
# HOMEWORK
# ==========================================

HOMEWORK_PROMPT = """
Create a complete NCF 2023 aligned homework assignment.

Topic:
{topic}

Student Level:
{student_level}

Generate the following sections:

1. Homework Information

- Topic Name
- Class Level
- Estimated Completion Time

2. Learning Outcomes Reinforced

Explain the concepts and skills students will strengthen through this homework.

3. Competencies Developed

Examples:
- Critical Thinking
- Problem Solving
- Observation
- Communication
- Creativity
- Decision Making
- Application of Knowledge

4. Practice Questions

A. Easy Level Questions
- Recall-based questions
- Basic understanding questions

B. Moderate Level Questions
- Concept application questions
- Short reasoning questions

C. Hard Level Questions
- Higher-order thinking questions
- Real-life problem-solving questions

5. Activity-Based Homework

Include:
- Objective
- Materials Required
- Procedure
- Expected Learning

6. Observation-Based Homework

Encourage students to observe their surroundings and connect learning with real life.

7. Reflection Question

Provide self-reflection questions that encourage thinking and self-assessment.

8. Real-Life Application Task

Ask students to apply the concept in daily life situations.

9. Parent Involvement Suggestion

Provide an optional activity that encourages discussion with parents or family members.

10. Self-Assessment Checklist

Students can evaluate:
- I understood the topic.
- I completed all activities.
- I can explain the concept to others.
- I can apply the concept in daily life.

Requirements:

- Follow NCF 2023 principles
- Student-friendly language
- Age-appropriate tasks
- Encourage conceptual understanding
- Encourage critical thinking
- Avoid rote memorization
- Focus on application and exploration
- Include experiential learning opportunities
- Classroom and home-friendly activities
"""

# ==========================================
# WORKSHEET
# ==========================================

WORKSHEET_PROMPT = """
Create a complete NCF 2023 aligned worksheet.

Content:
{content}

Student Level:
{student_level}

Generate the following sections:

1. Worksheet Information

- Topic Name
- Class Level
- Estimated Time

2. Learning Outcomes

Clearly state what students should know and be able to do.

3. Competencies Developed

Examples:
- Critical Thinking
- Communication
- Observation
- Problem Solving
- Creativity
- Logical Thinking

4. Fill in the Blanks

Generate 10 competency-based questions.

5. Match the Following

Generate 10 matching items.

6. True or False

Generate 10 concept-based statements.

7. Short Answer Questions

Generate 10 short-answer questions.

8. Easy Questions

Recall and understanding-based questions.

9. Moderate Questions

Application-based questions.

10. Hard Questions

Analysis and reasoning-based questions.

11. HOTS Questions

Generate Higher Order Thinking Skills questions.

12. Activity-Based Task

Include:
- Objective
- Materials Needed
- Procedure
- Learning Outcome

13. Real-Life Application Task

Connect learning with daily life situations.

14. Reflection Question

Encourage students to think about what they learned.

15. Self-Assessment Checklist

Students evaluate their understanding.

Requirements:

- Follow NCF 2023 principles
- Competency-based learning
- Concept-focused questions
- Classroom-friendly format
- Age-appropriate language
- Well-structured sections
- Encourage higher-order thinking
- Focus on understanding rather than memorization
"""

# ==========================================
# BLOOM TAXONOMY
# ==========================================

BLOOM_PROMPT = """
Create NCF 2023 aligned Bloom's Taxonomy questions.

Topic:
{topic}

Student Level:
{student_level}

Generate questions for all six Bloom's Taxonomy levels:

1. Remember

Generate:
- Question
- Expected Answer
- Learning Skill
- Competency Developed

2. Understand

Generate:
- Question
- Expected Answer
- Learning Skill
- Competency Developed

3. Apply

Generate:
- Question
- Real-Life Application
- Learning Skill
- Competency Developed

4. Analyze

Generate:
- Question
- Analysis Requirement
- Learning Skill
- Competency Developed

5. Evaluate

Generate:
- Question
- Evaluation Requirement
- Learning Skill
- Competency Developed

6. Create

Generate:
- Question
- Creative Task
- Learning Skill
- Competency Developed

Additional Sections:

7. Learning Outcomes

8. Competencies Developed

9. Teacher Notes

Explain how these questions support competency-based learning.

Requirements:

- Follow NCF 2023 principles
- Progressive difficulty levels
- Competency-based assessment
- Encourage critical thinking
- Encourage creativity and innovation
- Focus on conceptual understanding
- Promote higher-order thinking skills
- Use student-friendly language
- Classroom-ready format
"""

# ==========================================
# WEB SEARCH ANSWER
# ==========================================

WEB_SEARCH_PROMPT = """
Answer the user's question using the provided web search content.

Question:
{question}

Web Content:
{web_content}

Generate the following sections:

1. Topic Overview

Provide a simple and easy-to-understand explanation.

2. Simple Explanation

Explain the concept in age-appropriate language.

3. Key Points

Summarize the most important information.

4. Real-Life Examples

Provide relatable examples from daily life.

5. Learning Outcomes

After reading this content, students should be able to:

- Outcome 1
- Outcome 2
- Outcome 3

6. Competencies Developed

Examples:
- Observation
- Communication
- Critical Thinking
- Problem Solving
- Information Literacy

7. Activity Suggestion

Provide an engaging classroom or home activity related to the topic.

Include:
- Objective
- Materials Needed
- Procedure
- Expected Learning

8. Quick Assessment Questions

Generate:
- Easy Questions
- Moderate Questions
- Challenging Questions

9. Reflection Question

Encourage students to connect learning with their experiences.

10. Teacher Notes

Provide guidance on how teachers can use this information effectively.

Requirements:

- Clearly mention that information comes from web sources.
- Follow NCF 2023 principles.
- Use simple and student-friendly language.
- Teacher-friendly format.
- Concept-focused explanation.
- Encourage inquiry and exploration.
- Default explanation level should be Class 5 unless another level is specified.
- Avoid complex technical language.
- Make the content classroom-ready.
"""

