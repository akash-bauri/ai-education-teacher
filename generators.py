# ==========================================
# generators.py
# ==========================================

from llm_service import call_llm


# ==========================================
# COMMON GENERATOR
# ==========================================

def generate_content(
    prompt,
    max_tokens=1500
):
    """
    Common wrapper for all generators.
    """

    return call_llm(
        prompt,
        max_tokens
    )


# ==========================================
# LEARNING OUTCOMES (UPDATED)
# ==========================================

def generate_learning_outcomes(
    topic,
    student_level="Class 5"
):

    prompt = f"""
Generate NCF 2023 aligned Learning Outcomes.

TOPIC:
{topic}

STUDENT LEVEL:
{student_level}

Structure:
Curricular Goal
↓
Competencies
↓
Learning Outcomes
↓
Assessment Indicators

Generate:

# Curricular Goal

# Competency Mapping

# Knowledge Outcomes

# Skill Outcomes

# Application Outcomes

# Assessment Indicators

Use action verbs:
- Explain
- Identify
- Compare
- Analyze
- Apply
- Evaluate
- Create
"""

    return generate_content(
        prompt,
        1200
    )


# ==========================================
# COMPETENCIES (UPDATED)
# ==========================================

def generate_competencies(
    topic,
    student_level="Class 5"
):

    prompt = f"""
Generate NCF 2023 aligned competencies.

TOPIC:
{topic}

STUDENT LEVEL:
{student_level}

Include these Competencies:
# Critical Thinking
# Communication
# Problem Solving
# Collaboration
# Observation
# Creativity
# Reasoning
# Art Integrated Learning
# Game Based Learning
# Real Life Application
# Inquiry Based Learning
# Self Learning

For every competency provide:
- Description
- Classroom Application
- Student Behaviour Indicators
- Assessment Evidence
"""

    return generate_content(
        prompt,
        1200
    )


# ==========================================
# LESSON PLAN (UPDATED)
# ==========================================

def generate_lesson_plan(
    topic,
    student_level="Class 5"
):

    prompt = f"""
TOPIC:
{topic}

STUDENT LEVEL:
{student_level}

IMPORTANT:
Generate a highly detailed lesson plan.
Minimum length: 3000+ words
Do not generate generic content.
Extract actual chapter name whenever possible.

Create a complete NCF 2023 aligned lesson plan.

# 1. Curricular Goal

# 2. Competencies

# 3. Learning Outcomes

# 4. Assessment Indicators

# 5. Competency Mapping

Generate detailed competency mapping aligned with NCF 2023.
For each competency include:
* Competency Description
* Classroom Application
* Student Behaviour Indicators
* Assessment Evidence

## Critical Thinking
Explain how students analyze, compare, infer, classify, evaluate, and draw conclusions.

## Problem Solving
Explain how students apply concepts to solve real-life situations and classroom challenges.

## Communication Skills
Explain how students express ideas through speaking, writing, discussion, presentation, and visual communication.

## Collaboration
Explain how students work effectively in pairs, teams, and group activities.

## Creativity and Innovation
Explain how students generate ideas, design projects, create models, and develop original solutions.

## Self Learning
Explain how students independently explore concepts and reflect on their own learning.

## Digital Literacy
Explain how students use technology responsibly and effectively for learning.

## Observation and Inquiry
Explain how students observe, investigate, explore, and ask meaningful questions.

# Art Integrated Learning Competency
Explain how art helps students understand the topic through creative expression.

Generate Art Activities:
* Drawing Activity
* Coloring Activity
* Poster Making Activity
* Craft Activity
* Storytelling Activity
* Drama / Role Play Activity

For each activity provide:
* Objective
* Materials Required
* Procedure
* Expected Learning Outcome

# Game Based Learning Competency
Explain how games help students learn through play, participation, and engagement.

Generate Game Based Activities:
## Individual Game
Include: Game Name, Rules, Learning Objective, Assessment Method
## Pair Activity Game
Include: Game Name, Rules, Learning Objective, Assessment Method
## Group Activity Game
Include: Game Name, Rules, Learning Objective, Assessment Method
## Classroom Challenge
Include: Challenge Name, Procedure, Learning Objective, Assessment Method
## Quiz Competition
Include: Quiz Format, Rules, Learning Objective, Assessment Method

# Activity Details
Generate structured execution paths for:
- Individual Activity
- Pair Activity
- Group Activity

# Real Life Application Competency
Generate at least 10 practical real-life applications.
Explain how students can connect the concept to daily life, community, environment, home, school, and future learning.

# Reflection Activities
Generate processing prompts and reflection checkpoints for students.

# Assessment Rubrics
Provide a comprehensive matrix marking across these levels:
- Beginning
- Developing
- Proficient
- Advanced

IMPORTANT:
Art Integrated Learning and Game Based Learning are mandatory.
Generate detailed classroom-ready activities.
Do not give generic answers.
Provide practical examples that teachers can directly use in the classroom.
"""

    return generate_content(
        prompt,
        4500
    )


# ==========================================
# TEACHING GUIDE (UPDATED)
# ==========================================

def generate_teaching_guide(
    topic,
    student_level="Class 5",
    teaching_style="Beginner Friendly"
):

    prompt = f"""
Create a complete NCF 2023 aligned teaching guide.

TOPIC:
{topic}

STUDENT LEVEL:
{student_level}

TEACHING STYLE:
{teaching_style}

Generate:

# Chapter Overview

# Curricular Goal

# Competencies

# Learning Outcomes

# Key Concepts

# Teacher Introduction Script

# Student Responses

# Detailed Topic Explanation

# Real Life Examples

# Activity Based Learning

# Art Activity

# Game Activity

# Reflection Activity

# Student Engagement Questions

# Common Misconceptions

# Inclusive Teaching Strategies

# Easy Questions

# Moderate Questions

# Hard Questions

# Assessment Suggestions

# Assessment Rubric

# Extension Activities

# Homework

# Recap

# Flow Chart

# Mind Map

Explain as if training a teacher.
"""

    return generate_content(
        prompt,
        3500
    )


# ==========================================
# FLOWCHART (UPDATED)
# ==========================================

def generate_flowchart(
    topic
):

    prompt = f"""
Generate an NCF 2023 aligned educational flowchart.

TOPIC:
{topic}

Structure:
Prior Knowledge
↓
Introduction
↓
Exploration
↓
Concept Building
↓
Activity
↓
Discussion
↓
Application
↓
Assessment
↓
Reflection
↓
Real Life Connection

Use arrows and clean formatting.
"""

    return generate_content(
        prompt,
        2200
    )


# ==========================================
# MIND MAP (UPDATED)
# ==========================================

def generate_mindmap(
    topic
):

    prompt = f"""
Generate an NCF 2023 aligned educational mind map.

TOPIC:
{topic}

Include:

Central Topic
├── Curricular Goal
├── Competencies
├── Learning Outcomes
├── Core Concepts
├── Real Life Applications
├── Activity Ideas
├── Art Activities
├── Game Activities
├── Reflection Activities
├── Assessment Ideas
├── Assessment Rubrics
└── Cross Curricular Connections

Use proper hierarchical structure.
"""

    return generate_content(
        prompt,
        2200
    )


# ==========================================
# CHAPTER SUMMARY (UPDATED)
# ==========================================

def generate_chapter_summary(
    topic
):

    prompt = f"""
Generate an NCF 2023 aligned chapter summary.

TOPIC:
{topic}

Include:

# Chapter Overview

# Learning Outcomes

# Competencies

# Key Concepts

# Important Definitions

# Important Formulas

# Real Life Applications

# Common Misconceptions

# Frequently Asked Questions

# Activity Suggestions

# Quick Revision Notes

# Summary

Use simple language.
"""

    return generate_content(
        prompt,
        2500
    )


# ==========================================
# IMPORTANT QUESTIONS (UPDATED)
# ==========================================

def generate_important_questions(
    topic
):

    prompt = f"""
Generate NCF 2023 aligned important questions.

TOPIC:
{topic}

Generate:

# Easy Questions
(Knowledge)
Provide 10 Easy Questions.

# Moderate Questions
(Understanding & Application)
Provide 10 Moderate Questions.

# Hard Questions
(Analysis & Evaluation)
Provide 10 Hard Questions.

# Competency Based Questions
Provide 10 Competency Based Questions.

# Case Based Questions
Provide 10 Case Based Questions.

# Assertion & Reason Questions
Provide 5 Assertion & Reason Questions.

# Multiple Correct Answer Questions
Provide 5 Multiple Correct Answer Questions.

# Real Life Application Questions
Provide 5 Real Life Application Questions.

# Activity Based Questions
"""

    return generate_content(
        prompt,
        4000
    )
