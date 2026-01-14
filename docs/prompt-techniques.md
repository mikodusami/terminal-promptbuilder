# Prompt Engineering Techniques

Prompt Builder supports 7 modern prompt engineering techniques. Each is optimized for different use cases.

## 1. Chain of Thought (CoT) 🧠

**Best for:** Complex reasoning, math problems, logic puzzles, multi-step analysis

**How it works:** Encourages the model to break down problems into steps and show its reasoning process.

**Generated structure:**

```
Context: [your context]

Task: [your task]

Think through this step-by-step:
1. First, identify the key elements of the problem
2. Break down the problem into smaller parts
3. Solve each part systematically
4. Combine the solutions and verify the result

Let's work through this carefully:

Constraints to consider:
- [your constraints]
```

**Example use cases:**

- Solving math word problems
- Debugging code logic
- Analyzing complex scenarios
- Making decisions with multiple factors

---

## 2. Few-Shot Learning 📚

**Best for:** Pattern recognition, consistent formatting, style matching, classification tasks

**How it works:** Provides examples that demonstrate the desired input-output pattern.

**Generated structure:**

```
Context: [your context]

Task: [your task]

Here are some examples:

Example 1:
Input: [example input]
Output: [example output]

Example 2:
Input: [example input]
Output: [example output]

Now, apply the same pattern to solve the following:
```

**Example use cases:**

- Text classification
- Data transformation
- Style transfer
- Format conversion

**Tips:**

- Provide 2-5 diverse examples
- Make examples representative of edge cases
- Keep examples consistent in format

---

## 3. Role-Based 🎭

**Best for:** Domain expertise, professional advice, specialized knowledge, persona-driven responses

**How it works:** Assigns a specific expert persona to the model, framing responses from that perspective.

**Generated structure:**

```
You are a [role/persona].

Background: [your context]

Your task: [your task]

Approach this with your expertise, providing:
- Professional insights
- Practical recommendations
- Clear explanations

Keep in mind:
- [your constraints]
```

**Example roles:**

- "senior software architect with 15 years experience"
- "medical researcher specializing in immunology"
- "financial advisor for small businesses"
- "UX designer focused on accessibility"

**Tips:**

- Be specific about experience level and specialization
- Include relevant credentials or background
- Specify the audience for the response

---

## 4. Structured Output 📋

**Best for:** API responses, data extraction, formatted reports, consistent schemas

**How it works:** Requests responses in a specific format (JSON, Markdown, tables, etc.)

**Generated structure:**

```
Context: [your context]

Task: [your task]

Provide your response in [format] format.

Structure your response with:
- Clear sections/fields
- Consistent formatting
- Complete information

Requirements:
- [your constraints]
```

**Supported formats:**

- JSON
- Markdown
- Tables
- XML
- YAML
- Custom schemas

**Tips:**

- Provide an example of the desired structure
- Specify required vs optional fields
- Include data type expectations

---

## 5. ReAct (Reasoning + Acting) ⚡

**Best for:** Multi-step tasks, research, tool use, iterative problem solving

**How it works:** Combines reasoning about what to do with taking actions and observing results.

**Generated structure:**

```
Context: [your context]

Task: [your task]

Use the ReAct framework to solve this:

For each step, follow this pattern:
Thought: [Your reasoning about what to do next]
Action: [The action you decide to take]
Observation: [What you observe from the action]
... (repeat until solved)
Final Answer: [Your conclusion]

Begin your analysis:
```

**Example use cases:**

- Research tasks
- Debugging with tool access
- Data analysis workflows
- Decision-making processes

---

## 6. Tree of Thoughts (ToT) 🌳

**Best for:** Creative problem solving, exploring alternatives, strategic planning

**How it works:** Explores multiple solution paths, evaluates each, and selects the best approach.

**Generated structure:**

```
Context: [your context]

Task: [your task]

Explore this problem using Tree of Thoughts:

1. Generate 3 different initial approaches
2. For each approach, evaluate:
   - Feasibility (1-10)
   - Potential issues
   - Expected outcome
3. Select the most promising path
4. Develop it further, backtracking if needed
5. Present your final solution with reasoning

Start by listing your three approaches:
```

**Example use cases:**

- Strategic planning
- Creative writing
- Architecture decisions
- Problem solving with uncertainty

---

## 7. Self-Consistency 🔄

**Best for:** Verification, high-stakes decisions, reducing errors, consensus building

**How it works:** Generates multiple independent solutions and identifies the most consistent answer.

**Generated structure:**

```
Context: [your context]

Task: [your task]

Apply self-consistency checking:

1. Solve this problem 3 different ways
2. For each solution, show your work
3. Compare all solutions
4. Identify the most consistent/reliable answer
5. Explain why this answer is most trustworthy

Solution 1:
```

**Example use cases:**

- Mathematical calculations
- Fact verification
- Critical decisions
- Quality assurance

---

## Choosing the Right Technique

| Scenario                | Recommended Technique       |
| ----------------------- | --------------------------- |
| Math/logic problems     | Chain of Thought            |
| Need consistent format  | Few-Shot Learning           |
| Domain expertise needed | Role-Based                  |
| API/data output         | Structured Output           |
| Multi-step research     | ReAct                       |
| Exploring options       | Tree of Thoughts            |
| High-stakes accuracy    | Self-Consistency            |
| Complex tasks           | Combine multiple techniques |
