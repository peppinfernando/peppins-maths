#!/usr/bin/env python3
"""
Peppin's Tuition Centre, Cork — Junior Cycle Maths Study App
Static site generator: run `python3 generate.py` to build the full app.
Output goes to ./docs/ — ready to publish on GitHub Pages.
"""

import json, os, shutil, textwrap
from pathlib import Path

OUT = Path("docs")

# ─── CURRICULUM DATA ───────────────────────────────────────────────────────────
DAYS = [
  { "day":1,"topic":"Natural Numbers","subtopic":"Place Value, Ordering & BEMDAS","level":"Foundation",
    "block":"Number","color":"#1B3A6B",
    "concept":{"explain":["Natural numbers are the counting numbers: 1, 2, 3, 4, 5… Place value tells us how much each digit is worth based on its POSITION in the number. The digit 4 in 4,000 is worth four thousand; in 40 it is worth only forty.","BEMDAS is the agreed ORDER of operations: Brackets → Exponents (powers) → Multiplication/Division (left to right) → Addition/Subtraction (left to right). Everyone must follow this rule or calculations give different answers."],"analogy":"BEMDAS is like traffic rules — without them, 2+3×4 could mean (2+3)×4=20 (wrong) or 2+(3×4)=14 (correct). The rule says: multiply BEFORE adding, so the answer is always 14.","worked":{"title":"Calculate 8 + 4 × (6 − 2)² − 3","steps":["Brackets first: (6 − 2) = 4","Exponents: 4² = 16","Multiply: 4 × 16 = 64","Add/Subtract left to right: 8 + 64 − 3 = 69","Answer: 69"]},"mistakes":["Never add before multiplying: 2+3×4 ≠ 20. Do 3×4=12 first, then add 2 → 14","In 3+2², the answer is 3+4=7, NOT (3+2)²=25","Always work INSIDE brackets before anything outside"],"formulae":["BEMDAS: Brackets → Exponents → Multiply/Divide → Add/Subtract","Place value: Units | Tens | Hundreds | Thousands"]},
    "questions":[
      {"q":1,"marks":2,"text":"Write 9,473 in expanded form using place value.","answer":"9,000 + 400 + 70 + 3 = 9,473","hint":"Think about what each digit is worth based on its column position."},
      {"q":2,"marks":2,"text":"Arrange in ascending order: 3,274  1,247  3,742  3,724  3,247","answer":"1,247  3,247  3,274  3,724  3,742","hint":"Compare the thousands digit first, then hundreds, etc."},
      {"q":3,"marks":3,"text":"Calculate: 7 + 9 × 4 − 2  (Show BEMDAS steps)","answer":"Multiply first: 9×4=36. Then: 7+36−2 = 41","hint":"Which BEMDAS operation comes first when there are no brackets?"},
      {"q":4,"marks":3,"text":"Calculate: (12 − 4) × 3 + 2²","answer":"Brackets: 8. Exponent: 4. Multiply: 8×3=24. Add: 24+4 = 28","hint":"Work through BEMDAS step by step: B, then E, then M, then A."},
      {"q":5,"marks":4,"text":"Calculate: 5 × [18 ÷ (3 + 3)] − 4. Show each step.","answer":"Inner brackets: 3+3=6. Division: 18÷6=3. Multiply: 5×3=15. Subtract: 15−4 = 11","hint":"Start with the innermost brackets first."},
      {"q":6,"marks":4,"text":"Evaluate 4² + 3³ and explain each step.","answer":"4²=16; 3³=27; 16+27 = 43","hint":"Calculate each power separately, then add."},
    ]
  },
  { "day":2,"topic":"Natural Numbers","subtopic":"Factors, Multiples, HCF & LCM","level":"Foundation",
    "block":"Number","color":"#1B3A6B",
    "concept":{"explain":["A FACTOR divides a number exactly with no remainder. For example 3 is a factor of 12 because 12÷3=4 exactly. A MULTIPLE is the result of multiplying a number by any whole number — multiples of 5 are 5, 10, 15, 20…","HCF (Highest Common Factor) = largest factor shared. LCM (Lowest Common Multiple) = smallest shared multiple. Use PRIME FACTORISATION for both."],"analogy":"Making identical gift bags: if you have 36 sweets and 48 chocolates, the HCF (12) tells you the MAXIMUM number of bags. The LCM tells you when two repeating schedules first coincide — like buses departing at different intervals.","worked":{"title":"Find HCF and LCM of 36 and 48","steps":["Prime factorise 36: 2² × 3²","Prime factorise 48: 2⁴ × 3","HCF = LOWEST powers of shared primes: 2² × 3 = 12","LCM = HIGHEST powers of all primes: 2⁴ × 3² = 144","Check: 144÷36=4 ✓  and  144÷48=3 ✓"]},"mistakes":["HCF → LOWEST powers. LCM → HIGHEST powers. Students swap these constantly!","1 is NOT a prime number (only one factor: itself)","List factors in pairs: 1×24, 2×12, 3×8, 4×6 — stop when the pair meets"],"formulae":["HCF = product of shared primes at LOWEST powers","LCM = product of ALL primes at HIGHEST powers","For two numbers: HCF × LCM = a × b"]},
    "questions":[
      {"q":1,"marks":2,"text":"List ALL factors of 24.","answer":"1, 2, 3, 4, 6, 8, 12, 24","hint":"Find factor pairs: 1×24, 2×12, 3×8, 4×6..."},
      {"q":2,"marks":2,"text":"Write the first five multiples of 7.","answer":"7, 14, 21, 28, 35","hint":"Multiply 7 by 1, 2, 3, 4, 5."},
      {"q":3,"marks":3,"text":"Find the HCF of 36 and 48 using prime factorisation.","answer":"36=2²×3²; 48=2⁴×3; HCF = 2²×3 = 12","hint":"Write each as a product of primes. Take LOWEST powers of shared primes."},
      {"q":4,"marks":3,"text":"Find the LCM of 36 and 48 using prime factorisation.","answer":"36=2²×3²; 48=2⁴×3; LCM = 2⁴×3² = 144","hint":"Take HIGHEST powers of ALL primes that appear."},
      {"q":5,"marks":4,"text":"Bus A leaves every 12 minutes, Bus B every 18 minutes. Both depart at 9:00 am. When do they next depart together?","answer":"LCM(12,18)=36 minutes. Next joint departure: 9:36 am","hint":"The buses meet again after LCM minutes."},
      {"q":6,"marks":4,"text":"Find the HCF and LCM of 12, 18 and 30.","answer":"12=2²×3; 18=2×3²; 30=2×3×5. HCF=6; LCM=180","hint":"Factorise all three, then apply HCF and LCM rules to three numbers."},
    ]
  },
  { "day":3,"topic":"Integers","subtopic":"Directed Numbers & Operations","level":"Foundation",
    "block":"Number","color":"#1B3A6B",
    "concept":{"explain":["Integers: …−3, −2, −1, 0, 1, 2, 3,… Negative numbers sit to the LEFT of zero on the number line.","Adding a negative = moving LEFT. Subtracting a negative = moving RIGHT (like adding). Multiplication: SAME signs→POSITIVE. DIFFERENT signs→NEGATIVE."],"analogy":"Temperature: if it is −5°C and drops 3 more degrees you get −8°C. 'How much warmer is 4°C than −3°C?' Answer: 4−(−3)=4+3=7 degrees warmer. Subtracting a negative equals adding!","worked":{"title":"Evaluate 8 + (−3)×(−2) − (−1)","steps":["BEMDAS — Multiply first: (−3)×(−2) = +6  [same signs]","Rewrite: 8 + 6 − (−1)","Subtracting negative: 8 + 6 + 1","Final answer: 15"]},"mistakes":["(−)×(−) = POSITIVE. Two negatives multiplied always give positive.","5−(−3) = 5+3 = 8. NOT 5−3=2.","On number line: −2 is GREATER than −7 (further right)"],"formulae":["(+)×(+)=(+)  |  (−)×(−)=(+)","(+)×(−)=(−)  |  a−(−b)=a+b"]},
    "questions":[
      {"q":1,"marks":2,"text":"Calculate: −7 + 3","answer":"−7 + 3 = −4","hint":"Move 3 steps to the RIGHT of −7 on the number line."},
      {"q":2,"marks":2,"text":"Calculate: 5 − (−3)","answer":"5 − (−3) = 5 + 3 = 8","hint":"Subtracting a negative is the same as adding."},
      {"q":3,"marks":3,"text":"Calculate: (−4) × (−6)","answer":"(−4) × (−6) = +24 (same signs give positive)","hint":"Same signs → positive result."},
      {"q":4,"marks":3,"text":"Calculate: −18 ÷ 3","answer":"−18 ÷ 3 = −6 (different signs give negative)","hint":"Negative ÷ positive = negative."},
      {"q":5,"marks":4,"text":"Evaluate: 8 + (−3) × (−2) − (−1). Use BEMDAS and show each step.","answer":"Multiply: (−3)×(−2)=+6. Rewrite: 8+6−(−1)=8+6+1=15","hint":"Do the multiplication first, then deal with the signs."},
      {"q":6,"marks":4,"text":"Monday was −5°C. Tuesday was 8° warmer. Wednesday was 11° colder than Tuesday. Which day was coldest?","answer":"Tue: −5+8=3°C. Wed: 3−11=−8°C. Coldest=Wednesday (−8°C).","hint":"Calculate each day's temperature in order."},
    ]
  },
  { "day":4,"topic":"Fractions","subtopic":"All Four Operations with Fractions","level":"Foundation→Ordinary",
    "block":"Number","color":"#1B3A6B",
    "concept":{"explain":["ADD/SUBTRACT fractions: find the LCD (lowest common denominator), convert each fraction, then combine numerators only.","MULTIPLY: straight across (numerator × numerator, denominator × denominator).","DIVIDE: flip the second fraction (find its reciprocal) and then multiply.","Always simplify your final answer."],"analogy":"Adding fractions without a common denominator is like adding thirds and quarters of a pizza without cutting them the same size. The LCD tells you what size to cut all slices — then you can add them fairly.","worked":{"title":"Calculate (3/4) ÷ (3/8)","steps":["Flip second fraction: 3/8 becomes 8/3","Change ÷ to ×: (3/4) × (8/3)","Multiply across: 24/12","Simplify: 24/12 = 2","Check: how many 3/8 fit in 3/4? Answer: 2 ✓"]},"mistakes":["NEVER add denominators: 1/3+1/4 ≠ 2/7. Find the LCD first!","When multiplying: do NOT find a common denominator","Always simplify to lowest terms"],"formulae":["a/b + c/d = (ad+bc)/bd  [use LCD method]","(a/b)×(c/d) = ac/bd","(a/b)÷(c/d) = (a/b)×(d/c)"]},
    "questions":[
      {"q":1,"marks":2,"text":"Simplify 12/18 to its lowest terms.","answer":"HCF(12,18)=6; 12/18 = 2/3","hint":"Divide both top and bottom by the HCF."},
      {"q":2,"marks":3,"text":"Calculate: 1/4 + 2/3","answer":"LCD=12; 3/12+8/12 = 11/12","hint":"Find LCD, convert both fractions, then add numerators."},
      {"q":3,"marks":3,"text":"Calculate: 3/5 − 1/4","answer":"LCD=20; 12/20−5/20 = 7/20","hint":"LCD of 5 and 4 is 20."},
      {"q":4,"marks":3,"text":"Calculate: (2/3) × (3/5)","answer":"(2×3)/(3×5) = 6/15 = 2/5","hint":"Multiply numerators together and denominators together."},
      {"q":5,"marks":3,"text":"Calculate: (3/4) ÷ (3/8)","answer":"(3/4)×(8/3) = 24/12 = 2","hint":"Flip the second fraction, then multiply."},
      {"q":6,"marks":4,"text":"In a class of 60 students, 1/3 prefer football and 1/4 prefer rugby. How many prefer other sports?","answer":"Football: 20. Rugby: 15. Other: 60−20−15 = 25 students","hint":"Find 1/3 and 1/4 of 60 separately, then subtract from total."},
    ]
  },
  { "day":5,"topic":"Decimals & Percentages","subtopic":"Conversions, Rounding & % Change","level":"Foundation→Ordinary",
    "block":"Number","color":"#1B3A6B",
    "concept":{"explain":["Fraction→Decimal: divide top by bottom. Decimal→%: multiply by 100. %→Decimal: divide by 100.","Rounding: look at the digit AFTER the required place. If ≥5, round up. If ≤4, keep same.","% change = (change ÷ ORIGINAL) × 100. Multiplier for x% increase: (1+x/100). Decrease: (1−x/100)."],"analogy":"Two successive discounts are NOT the same as one combined discount. A 20% then 35% discount on €200 gives €104 — NOT 55% off (which would be €90). The second discount acts on an already-reduced price!","worked":{"title":"€200 coat reduced 20% then 35%. Final price?","steps":["After 20%: €200 × 0.80 = €160","After 35% (on new price): €160 × 0.65 = €104","Final = €104","WARNING: 20%+35%=55% → €200×0.45=€90 is WRONG!"]},"mistakes":["% change: divide by the ORIGINAL, not the new value","Two successive discounts ≠ one combined discount","Rounding 3.745 to 2 d.p.: look at 3rd decimal (5) → round UP → 3.75"],"formulae":["% Change = (Change÷Original)×100","Multiplier: increase=(1+x/100); decrease=(1−x/100)","Compound interest: A = P(1+r/100)ⁿ"]},
    "questions":[
      {"q":1,"marks":2,"text":"Convert 3/8 to a decimal and a percentage.","answer":"3÷8=0.375; 0.375×100=37.5%","hint":"Divide 3 by 8, then multiply by 100."},
      {"q":2,"marks":2,"text":"Round 3.4756 to 2 decimal places.","answer":"Look at 3rd decimal (5): round UP → 3.48","hint":"Look at the THIRD decimal place to decide whether to round up or keep."},
      {"q":3,"marks":3,"text":"Find 15% of €240.","answer":"0.15 × 240 = €36","hint":"Convert 15% to a decimal (0.15) then multiply."},
      {"q":4,"marks":3,"text":"A price rises from €200 to €225. Find the percentage increase.","answer":"Change=€25; (25÷200)×100 = 12.5%","hint":"Divide the CHANGE by the ORIGINAL, then multiply by 100."},
      {"q":5,"marks":4,"text":"A coat costs €200. Reduced by 20% then reduced by 35% in a sale. Find the final price.","answer":"After 20%: €200×0.80=€160. After 35%: €160×0.65=€104","hint":"Apply each discount separately. The second discount is on the NEW price."},
      {"q":6,"marks":4,"text":"€5,000 is invested at 3% compound interest per year. Find the value after 2 years.","answer":"Year 1: €5,000×1.03=€5,150. Year 2: €5,150×1.03=€5,304.50","hint":"Each year, multiply the PREVIOUS year's total by 1.03."},
    ]
  },
  { "day":6,"topic":"Number Systems & Sets","subtopic":"N, Z, Q, R and Venn Diagrams","level":"Ordinary",
    "block":"Number","color":"#1B3A6B",
    "concept":{"explain":["N={1,2,3,…} ⊂ Z={…,−2,−1,0,1,2,…} ⊂ Q={all fractions p/q, q≠0} ⊂ R={all real numbers, including irrationals like √2 and π}.","Venn diagrams show set relationships. A∪B = 'A OR B'. A∩B = 'A AND B'. Formula: |A∪B|=|A|+|B|−|A∩B|."],"analogy":"The number sets are Russian nesting dolls: N fits inside Z, which fits inside Q, which fits inside R. Every natural number is also an integer, a rational number and a real number.","worked":{"title":"30 students: 18 study French, 20 Spanish, 12 both. How many study neither?","steps":["Place 12 in the overlap (both)","French only: 18−12=6","Spanish only: 20−12=8","Total in circles: 6+12+8=26","Neither: 30−26 = 4 students"]},"mistakes":["Fill Venn diagrams: place INTERSECTION (both) FIRST, then find 'only A' and 'only B'","√4=2 ∈ N,Z,Q,R (rational). √5 is irrational — ∈ R only","Formula: |A∪B|=|A|+|B|−|A∩B| — subtract the overlap!"],"formulae":["N ⊂ Z ⊂ Q ⊂ R","|A∪B|=|A|+|B|−|A∩B|","Complement: P(A')=1−P(A)"]},
    "questions":[
      {"q":1,"marks":2,"text":"State which number set(s) contain: (i) √4  (ii) √5","answer":"√4=2 ∈ N,Z,Q,R. √5 is irrational → ∈ R only","hint":"Is each number a whole number? A fraction? Or does it never end without repeating?"},
      {"q":2,"marks":2,"text":"A={1,2,3,5,7}, B={3,4,5,6}. Find A∩B.","answer":"A∩B = {3,5}","hint":"List the elements that appear in BOTH sets."},
      {"q":3,"marks":3,"text":"Using the sets from Q2, find A∪B.","answer":"A∪B = {1,2,3,4,5,6,7}","hint":"List ALL elements from both sets (no duplicates)."},
      {"q":4,"marks":3,"text":"35 students: 20 play hockey, 23 play camogie, 8 play both. How many play at least one sport?","answer":"|H∪C|=20+23−8=35. All 35 students play at least one sport.","hint":"Use |A∪B|=|A|+|B|−|A∩B|."},
      {"q":5,"marks":4,"text":"Draw a Venn diagram for Q4. How many play neither?","answer":"Hockey only:12, Both:8, Camogie only:15. Total=35. Neither=0.","hint":"Fill in the overlap first (8), then find each circle's exclusive section."},
      {"q":6,"marks":4,"text":"Classify each: −3/4, 0, π, 2.5, −7","answer":"−3/4:Q,R. 0:Z,Q,R. π:R only. 2.5:Q,R. −7:Z,Q,R","hint":"Work through each number set from innermost (N) outward."},
    ]
  },
  { "day":7,"topic":"Applied Arithmetic","subtopic":"Ratio, Proportion, Currency & Tax","level":"Ordinary",
    "block":"Number","color":"#1B3A6B",
    "concept":{"explain":["RATIO: to divide in a ratio, find total parts, calculate one part, multiply. DIRECT proportion: both quantities scale together. INVERSE proportion: one increases as the other decreases.","CURRENCY: multiply by exchange rate (€→foreign). IRISH TAX: 20% on first €36,800; 40% on rest. Subtract tax credits AFTER calculating gross tax."],"analogy":"Ratio is like a recipe. Flour:oats=3:5 for 4 people. For 24 people (6× bigger), you need 18 cups flour and 30 cups oats. The ratio stays fixed; the amounts scale.","worked":{"title":"Divide €560 in the ratio 3:4:7","steps":["Total parts: 3+4+7 = 14","One part: €560÷14 = €40","First: 3×€40 = €120","Second: 4×€40 = €160","Third: 7×€40 = €280","Check: 120+160+280=560 ✓"]},"mistakes":["Always ADD parts before dividing the total","Inverse proportion: MORE workers=FEWER days. Use 1 worker first.","Tax credits reduce the TAX calculated, not the gross income"],"formulae":["Ratio: 1 part=total÷sum of parts","Direct: a₁/b₁=a₂/b₂","Tax payable=gross tax−tax credits"]},
    "questions":[
      {"q":1,"marks":2,"text":"Divide €400 in the ratio 3:5.","answer":"8 parts total; 1 part=€50; A=€150, B=€250","hint":"Add the ratio parts first: 3+5=8. Then find one part: €400÷8."},
      {"q":2,"marks":3,"text":"4 workers complete a job in 6 days. How long would 8 workers take? (Inverse proportion)","answer":"1 worker: 4×6=24 days. 8 workers: 24÷8=3 days","hint":"More workers = fewer days. Find how long for 1 worker first."},
      {"q":3,"marks":3,"text":"Convert €500 to dollars at €1=$1.12.","answer":"€500 × 1.12 = $560","hint":"Multiply by the exchange rate to convert FROM euro."},
      {"q":4,"marks":3,"text":"Gross salary €42,000. Tax: 20% on first €36,800; 40% on balance. Tax credits €3,550. Find tax payable.","answer":"Tax@20%=€7,360. Tax@40% on €5,200=€2,080. Gross tax=€9,440. Less credits: €5,890","hint":"Calculate each tax band separately, add them, then subtract credits."},
      {"q":5,"marks":4,"text":"Laptop costs €120 before VAT at 23%. Find the total price.","answer":"VAT=€120×0.23=€27.60. Total=€147.60","hint":"Multiply by the VAT rate to find the VAT amount, then add to original price."},
      {"q":6,"marks":4,"text":"Cement:sand:gravel = 1:2:4. 840 kg needed. How much of each?","answer":"7 parts; 1 part=120 kg; Cement=120, Sand=240, Gravel=480 kg","hint":"7 total parts. Find 1 part first, then multiply for each ingredient."},
    ]
  },
  { "day":8,"topic":"Algebra","subtopic":"Simplifying Expressions & Substitution","level":"Foundation",
    "block":"Algebra","color":"#2E7D32",
    "concept":{"explain":["LIKE TERMS have exactly the same variable and power. You can ONLY add/subtract like terms. 3x+5x=8x but 3x+5y cannot be combined.","SUBSTITUTE: replace every variable with the given number value. Always use BRACKETS around negative numbers to avoid sign errors."],"analogy":"Think of 'x' as a mystery box. 3x+2x = '3 boxes + 2 boxes = 5 boxes'. But 3x+2y is '3 boxes + 2 bags' — different objects, cannot be combined.","worked":{"title":"Evaluate 3a² − 2ab + b when a=2, b=−3","steps":["Substitute: 3(2)²−2(2)(−3)+(−3)","Exponents: 3(4)−2(2)(−3)+(−3)","Multiply: 12−(−12)+(−3)","Signs: 12+12−3","Answer: 21"]},"mistakes":["3a+5b−2a = a+5b: collect a-terms, leave 5b alone","Substituting negative: x=−3 means (−3)²=9, NOT −3²=−9","2x² means 2×(x²), NOT (2x)²=4x²"],"formulae":["Like terms: same variable and power","Simplify: collect like terms","Substitute: replace each variable, then BEMDAS"]},
    "questions":[
      {"q":1,"marks":2,"text":"Simplify: 3a + 5b − 2a + b","answer":"a + 6b","hint":"Group the a-terms and the b-terms separately."},
      {"q":2,"marks":2,"text":"Simplify: 5x² − 3x + x² + 4x","answer":"6x² + x","hint":"Collect x² terms together and x terms together."},
      {"q":3,"marks":3,"text":"Evaluate 2x² − 3x + 4 when x = 3.","answer":"2(9)−3(3)+4 = 18−9+4 = 13","hint":"Replace every x with 3. Use brackets and BEMDAS."},
      {"q":4,"marks":3,"text":"Find 3a² + 2ab − b² when a=2, b=−3.","answer":"3(4)+2(2)(−3)−(9) = 12−12−9 = −9","hint":"Put negative values in brackets when substituting."},
      {"q":5,"marks":4,"text":"Simplify: 3(2x − 1) − 2(x + 4)","answer":"6x−3−2x−8 = 4x − 11","hint":"Expand each bracket first, being careful with the minus sign before the second bracket."},
      {"q":6,"marks":4,"text":"P = 2(l+w). If l=3x+1 and w=x−2, express P simplified in terms of x.","answer":"P=2(3x+1+x−2)=2(4x−1)=8x−2","hint":"Substitute expressions for l and w, simplify inside brackets, then multiply by 2."},
    ]
  },
  { "day":9,"topic":"Algebra","subtopic":"Expanding Brackets","level":"Ordinary",
    "block":"Algebra","color":"#2E7D32",
    "concept":{"explain":["To expand (a+b)(c+d): use FOIL — First, Outer, Inner, Last. Then collect like terms.","Special patterns: (a+b)²=a²+2ab+b²; (a−b)²=a²−2ab+b²; (a+b)(a−b)=a²−b² (Difference of Two Squares)."],"analogy":"Expanding brackets is like distributing food: 3×(2 burgers+5 chips) = 6 burgers + 15 chips. With double brackets, EVERY person in the first group shakes hands with EVERY person in the second group.","worked":{"title":"Expand (2x−3)(3x+4)","steps":["F (First×First): 2x×3x = 6x²","O (Outer): 2x×4 = +8x","I (Inner): −3×3x = −9x","L (Last×Last): −3×4 = −12","Combine: 6x²+8x−9x−12","Answer: 6x² − x − 12"]},"mistakes":["(x+3)² ≠ x²+9. Must be x²+6x+9 — never skip the middle '2ab' term!","−2(x+4) means −2x−8. The negative applies to BOTH terms.","Always collect Outer+Inner terms (the x-terms) at the end"],"formulae":["(a+b)²=a²+2ab+b²","(a−b)²=a²−2ab+b²","(a+b)(a−b)=a²−b²  [DoTS]"]},
    "questions":[
      {"q":1,"marks":2,"text":"Expand: 3x(2x − 5)","answer":"6x² − 15x","hint":"Multiply 3x by each term inside the bracket."},
      {"q":2,"marks":3,"text":"Expand: (x + 3)(x + 5)","answer":"x²+5x+3x+15 = x²+8x+15","hint":"Use FOIL: First, Outer, Inner, Last."},
      {"q":3,"marks":3,"text":"Expand and simplify: (2x − 1)(3x + 4)","answer":"6x²+8x−3x−4 = 6x²+5x−4","hint":"Apply FOIL carefully with the negative sign."},
      {"q":4,"marks":3,"text":"Expand: (x + 5)²","answer":"x²+10x+25","hint":"Use (a+b)²=a²+2ab+b² with a=x, b=5."},
      {"q":5,"marks":4,"text":"Expand and simplify: (3x − 2)²","answer":"9x²−12x+4","hint":"Use (a−b)²=a²−2ab+b² with a=3x, b=2."},
      {"q":6,"marks":4,"text":"Expand: (2x+3)(2x−3). What pattern is this called?","answer":"4x²−9. This is the Difference of Two Squares: (a+b)(a−b)=a²−b²","hint":"Notice the middle terms cancel out."},
    ]
  },
  { "day":10,"topic":"Algebra","subtopic":"Factorising Expressions","level":"Ordinary",
    "block":"Algebra","color":"#2E7D32",
    "concept":{"explain":["FACTORISING is the reverse of expanding. Method 1 — Common Factor: find HCF of all terms, take outside. Method 2 — Trinomial: find two numbers with product=constant and sum=middle coefficient. Method 3 — Difference of Two Squares: a²−b²=(a+b)(a−b)."],"analogy":"Factorising is like working backwards from a cake to find the original ingredients. You know the expression (the cake) — what brackets (ingredients) multiplied to make it?","worked":{"title":"Factorise x² + 5x − 14","steps":["Need: product=−14, sum=+5","Test pairs: (−2,+7): product=−14 ✓, sum=+5 ✓","Factors: (x−2)(x+7)","Check: x²+7x−2x−14=x²+5x−14 ✓"]},"mistakes":["Always CHECK by expanding back out — 10 seconds, can save the question","Take the HIGHEST common factor, not just any","DoTS only works with a MINUS sign: x²+9 does NOT factorise"],"formulae":["Common factor: ax+ay=a(x+y)","Trinomial: x²+bx+c=(x+p)(x+q) where p+q=b, pq=c","DoTS: a²−b²=(a+b)(a−b)"]},
    "questions":[
      {"q":1,"marks":2,"text":"Factorise fully: 6x² − 9x","answer":"3x(2x−3)","hint":"Find the highest common factor of 6x² and 9x."},
      {"q":2,"marks":2,"text":"Factorise: x² − 49","answer":"(x+7)(x−7)  [Difference of Two Squares]","hint":"49=7². Use the DoTS pattern: a²−b²=(a+b)(a−b)."},
      {"q":3,"marks":3,"text":"Factorise: x² + 7x + 12","answer":"(x+3)(x+4)  [product=12, sum=7: 3×4=12, 3+4=7]","hint":"Find two numbers that multiply to 12 and add to 7."},
      {"q":4,"marks":3,"text":"Factorise: x² − 5x − 14","answer":"(x−7)(x+2)  [product=−14, sum=−5]","hint":"One number must be negative. Product=−14, sum=−5."},
      {"q":5,"marks":4,"text":"Factorise: 2x² + 7x + 3","answer":"(2x+1)(x+3)","hint":"Try factor pairs for 2x² and check if they give +7x when combined."},
      {"q":6,"marks":4,"text":"Factorise fully: 4x² − 25","answer":"(2x+5)(2x−5)  [DoTS: 4x²=(2x)², 25=5²]","hint":"Both terms are perfect squares with a minus sign between them."},
    ]
  },
  { "day":11,"topic":"Algebra","subtopic":"Solving Linear Equations & Inequalities","level":"Ordinary",
    "block":"Algebra","color":"#2E7D32",
    "concept":{"explain":["GOLDEN RULE: whatever you do to one side, do EXACTLY the same to the other. Inequalities: same rules EXCEPT when multiplying/dividing by a NEGATIVE — flip the inequality sign!"],"analogy":"An equation is a balanced seesaw. Whatever weight you add or remove from one side must be matched on the other. The solution is the value that keeps both sides exactly equal.","worked":{"title":"Solve 2(x+4) = 3x − 1","steps":["Expand: 2x+8=3x−1","Collect x-terms: 8=x−1","Add 1: 9=x  →  x=9","Check: LHS=2(13)=26. RHS=27−1=26 ✓"]},"mistakes":["Moving a term: always CHANGE its sign. +3x on left → −3x on right","Inequalities: −2x>6 → x<−3 (flip sign when dividing by negative!)","Always CHECK by substituting your answer back in"],"formulae":["Solve: ax+b=c → x=(c−b)/a","Flip inequality when ×÷ by negative","'Let x=…' — translate words to algebra first"]},
    "questions":[
      {"q":1,"marks":2,"text":"Solve: 3x − 7 = 11","answer":"3x=18; x=6","hint":"Add 7 to both sides, then divide by 3."},
      {"q":2,"marks":2,"text":"Solve: 2(x + 4) = 3x − 1","answer":"2x+8=3x−1; 9=x; x=9","hint":"Expand the bracket first, then collect like terms."},
      {"q":3,"marks":3,"text":"Solve: (x−1)/3 + (x+2)/4 = 5","answer":"LCD=12: 4(x−1)+3(x+2)=60 → 7x+2=60 → x=58/7","hint":"Multiply every term by the LCD (12) to clear the fractions."},
      {"q":4,"marks":3,"text":"Solve 2x − 5 < 9 and show on a number line.","answer":"2x<14 → x<7. Open circle at 7, arrow pointing left.","hint":"Solve like an equation. x<7 means open circle (not included) at 7."},
      {"q":5,"marks":4,"text":"Three times a number minus 8 equals twice the number plus 5. Find the number.","answer":"3n−8=2n+5 → n=13. Check: 39−8=31=26+5 ✓","hint":"Write 'Let n = the number', then translate each phrase to algebra."},
      {"q":6,"marks":4,"text":"A parent is 28 years older than their child. In 6 years, the parent will be twice the child's age. Find their current ages.","answer":"Let child=c: c+34=2(c+6) → c=22. Parent=50.","hint":"Set up equations using 'in 6 years' for both ages."},
    ]
  },
  { "day":12,"topic":"Algebra","subtopic":"Simultaneous Equations","level":"Ordinary",
    "block":"Algebra","color":"#2E7D32",
    "concept":{"explain":["SIMULTANEOUS EQUATIONS: two equations, two unknowns. Find the ONE pair of values satisfying BOTH at the same time.","ELIMINATION: multiply to match coefficients of one variable, then add/subtract to cancel it. SUBSTITUTION: rearrange one equation to 'x=…' and substitute into the other."],"analogy":"Simultaneous equations are like two clues in a puzzle — each alone has many answers, but combining them gives exactly ONE solution. Elimination is like cancelling one mystery by combining the clues.","worked":{"title":"Solve 3x+2y=12 and 5x−y=7","steps":["Multiply (ii)×2: 10x−2y=14 → (iii)","Add (i)+(iii): 13x=26 → x=2","Substitute into (i): 6+2y=12 → y=3","Check in (ii): 10−3=7 ✓"]},"mistakes":["Elimination: for cancellation, variable signs must be OPPOSITE (then add) or equal (then subtract)","ALWAYS check your answer in BOTH original equations","Substitution: substitute into the simpler equation"],"formulae":["Elimination: match coefficients → add/subtract","Substitution: rearrange one equation → substitute","Check: verify in BOTH equations"]},
    "questions":[
      {"q":1,"marks":4,"text":"Solve: 2x+y=7 and x−y=2","answer":"Add: 3x=9 → x=3. Sub: 3−y=2 → y=1. Check: 6+1=7 ✓","hint":"The y-terms are opposite signs — add the equations directly!"},
      {"q":2,"marks":4,"text":"Solve: 3x+2y=12 and 5x−y=7","answer":"Multiply (ii)×2: 10x−2y=14. Add: 13x=26 → x=2; y=3","hint":"Multiply the second equation by 2 to match the y-coefficient."},
      {"q":3,"marks":4,"text":"Solve: x+2y=8 and 3x−y=3","answer":"From (i): x=8−2y. Sub: 3(8−2y)−y=3 → 24−7y=3 → y=3; x=2","hint":"Use substitution: rearrange equation (i) to get x=… then substitute."},
      {"q":4,"marks":5,"text":"2 adults and 3 children pay €21.50 at the cinema. 4 adults and 1 child pay €26. Find adult and child ticket prices.","answer":"2a+3c=21.50; 4a+c=26. Multiply (ii)×3: 12a+3c=78. Subtract: 10a=56.50 → a=€5.65; c=€3.40","hint":"Let a=adult, c=child. Write two equations and solve simultaneously."},
      {"q":5,"marks":5,"text":"A farmer has chickens and cows. He counts 50 heads and 140 legs. How many of each?","answer":"c+w=50; 2c+4w=140 → c=30 chickens, w=20 cows","hint":"Chickens have 2 legs, cows have 4. Write one equation for heads and one for legs."},
      {"q":6,"marks":5,"text":"The sum of two numbers is 45. Their difference is 11. Find the two numbers.","answer":"a+b=45; a−b=11. Add: 2a=56 → a=28; b=17","hint":"Add both equations to eliminate b."},
    ]
  },
  { "day":13,"topic":"Algebra","subtopic":"Quadratic Equations","level":"Higher",
    "block":"Algebra","color":"#2E7D32",
    "concept":{"explain":["QUADRATIC: ax²+bx+c=0 (highest power is 2). Can have 0, 1 or 2 solutions.","Method 1 — Factorise. Method 2 — Quadratic Formula (in Tables booklet). ALWAYS rearrange to =0 first.","DISCRIMINANT: b²−4ac. >0 means 2 solutions; =0 means 1; <0 means none."],"analogy":"A quadratic describes a ball thrown in the air. Solutions are when height=0 (hits ground). Two solutions=hits ground at 2 points. One=grazes ground. None=never reaches ground level.","worked":{"title":"Solve 2x²+3x−4=0 using the quadratic formula","steps":["a=2, b=3, c=−4","Discriminant: 9+32=41","x=(−3±√41)/4","x₁≈0.85, x₂≈−2.35"]},"mistakes":["ALWAYS rearrange to =0 first","In formula: calculate √(b²−4ac) carefully","Negative solutions ARE valid unless context says otherwise (e.g. lengths must be positive)"],"formulae":["ax²+bx+c=0","x=[−b±√(b²−4ac)]/2a  (in Tables booklet)","Discriminant: b²−4ac"]},
    "questions":[
      {"q":1,"marks":3,"text":"Solve by factorising: x² − 5x + 6 = 0","answer":"(x−2)(x−3)=0 → x=2 or x=3","hint":"Find two numbers: product=6, sum=−5."},
      {"q":2,"marks":3,"text":"Solve by factorising: 2x² + x − 3 = 0","answer":"(2x+3)(x−1)=0 → x=−3/2 or x=1","hint":"Try factor pairs for the 2x² term."},
      {"q":3,"marks":4,"text":"Use the quadratic formula to solve: 2x²+3x−4=0 (to 2 d.p.)","answer":"x≈0.85 or x≈−2.35","hint":"Identify a=2, b=3, c=−4 and substitute into the formula."},
      {"q":4,"marks":4,"text":"Solve by completing the square: x²+6x+2=0","answer":"(x+3)²=7 → x=−3±√7","hint":"Complete the square: x²+6x = (x+3)²−9."},
      {"q":5,"marks":5,"text":"kx²−4x+4=0 has equal roots. Find k.","answer":"Equal roots: b²−4ac=0 → 16−16k=0 → k=1","hint":"Equal roots means the discriminant equals zero."},
      {"q":6,"marks":5,"text":"A rectangle has length 5m greater than its width. Area=84 m². Find dimensions.","answer":"x(x+5)=84 → x²+5x−84=0 → x=7 (positive). Width=7m, length=12m","hint":"Let width=x. Write area equation, rearrange to =0, solve."},
    ]
  },
  { "day":14,"topic":"Patterns & Sequences","subtopic":"Arithmetic Sequences","level":"Ordinary",
    "block":"Algebra","color":"#2E7D32",
    "concept":{"explain":["ARITHMETIC SEQUENCE: constant difference d between terms. nth TERM: Tₙ=a+(n−1)d. SUM of n terms: Sₙ=n/2×[2a+(n−1)d]."],"analogy":"A staircase with equal step heights. First step at height a, each step rises by d. The 10th step is at height a+9d. The formula is 'start + steps taken × step height'.","worked":{"title":"For 4,7,10,13,… find T₁₀ and S₁₀","steps":["a=4, d=3","Tₙ=4+(n−1)×3=3n+1","T₁₀=31","S₁₀=10/2×[8+27]=5×35=175"]},"mistakes":["Formula has (n−1)×d, NOT n×d","To check if a value is IN the sequence: set Tₙ=value, solve for n. Whole number=yes.","Sum formula uses a and d, not the last term"],"formulae":["Tₙ=a+(n−1)d","Sₙ=n/2×[2a+(n−1)d]","d=T₂−T₁"]},
    "questions":[
      {"q":1,"marks":2,"text":"Find the next three terms: 6, 11, 16, 21, …","answer":"d=5; next: 26, 31, 36","hint":"Find the common difference (d=11−6=5) and add it each time."},
      {"q":2,"marks":3,"text":"For 4,7,10,13,… find Tₙ and T₁₀.","answer":"Tₙ=3n+1; T₁₀=31","hint":"a=4, d=3. Use Tₙ=a+(n−1)d."},
      {"q":3,"marks":3,"text":"Is 2 a term in the sequence 100, 93, 86, 79, …?","answer":"Tₙ=107−7n. Set 107−7n=2 → n=15. Yes, 2 is the 15th term.","hint":"Find Tₙ, set it equal to 2, solve for n. If n is a whole number, yes!"},
      {"q":4,"marks":4,"text":"Find the sum of the first 15 terms of: 3, 8, 13, 18, …","answer":"a=3, d=5. S₁₅=15/2×[6+70]=7.5×76=570","hint":"Use the sum formula Sₙ=n/2×[2a+(n−1)d]."},
      {"q":5,"marks":4,"text":"Matchstick pattern: Diagram 1=4, D2=7, D3=10 sticks. How many for Diagram 20?","answer":"a=4, d=3; Tₙ=3n+1; T₂₀=61 sticks","hint":"Find a and d from the pattern, then find T₂₀."},
      {"q":6,"marks":5,"text":"3rd term=11 and 7th term=27. Find first term, d, and Tₙ.","answer":"T₃:a+2d=11; T₇:a+6d=27. Subtract:4d=16→d=4;a=3. Tₙ=4n−1","hint":"Write two equations for T₃ and T₇, then solve simultaneously."},
    ]
  },
  { "day":15,"topic":"Functions","subtopic":"Notation, Evaluation & Graphs","level":"Ordinary→Higher",
    "block":"Algebra","color":"#2E7D32",
    "concept":{"explain":["A FUNCTION maps each input (x) to exactly ONE output f(x). Evaluate by replacing every x with the given number and using BEMDAS.","GRAPH: make a table of values, plot points, draw smooth curve (quadratic) or straight line (linear). Roots=where f(x)=0. Vertex (min/max) of parabola: x=−b/2a."],"analogy":"A function is like a vending machine — press button x, get exactly one item f(x). It ALWAYS gives the same item for the same button.","worked":{"title":"Draw f(x)=x²−3x−4 for −1≤x≤4","steps":["Table: x=−1:0, x=0:−4, x=1:−6, x=2:−6, x=3:−4, x=4:0","Plot all points on a grid","Draw smooth parabola — NEVER a V-shape!","Roots at x=−1 and x=4"]},"mistakes":["Make a TABLE of at least 5 values — never sketch freehand","ROOTS=where f(x)=0, MINIMUM=lowest point — different things!","f(−3)=(−3)²=9, NOT −3²=−9"],"formulae":["Evaluate: replace x with given value","Roots: solve f(x)=0","Vertex: x=−b/2a"]},
    "questions":[
      {"q":1,"marks":2,"text":"If f(x)=2x²−5, find f(3).","answer":"2(9)−5=13","hint":"Replace x with 3 and calculate."},
      {"q":2,"marks":2,"text":"If g(x)=3x+1, find g(−2).","answer":"3(−2)+1=−5","hint":"Put −2 in brackets when substituting."},
      {"q":3,"marks":3,"text":"Find where f(x)=g(x) for f and g from Q1 and Q2 (to 2 d.p.).","answer":"2x²−5=3x+1 → 2x²−3x−6=0 → x≈2.64 or −1.14","hint":"Set the two functions equal and solve the resulting quadratic."},
      {"q":4,"marks":4,"text":"Draw h(x)=x²−3x+1 for −2≤x≤3 using a table of values.","answer":"x:−2(11),−1(5),0(1),1(−1),2(−1),3(1). Plot and draw smooth parabola.","hint":"Calculate y for each x value in the range, then plot."},
      {"q":5,"marks":4,"text":"Using your graph from Q4, find the minimum value of h(x).","answer":"Min at x=1.5; h(1.5)=2.25−4.5+1=−1.25","hint":"The minimum is the lowest point of the parabola (turning point)."},
      {"q":6,"marks":5,"text":"From your Q4 graph, estimate the roots of h(x)=0 to 1 d.p.","answer":"Roots ≈ x≈0.4 and x≈2.6 (where graph crosses x-axis)","hint":"Roots are where the graph crosses the x-axis (y=0)."},
    ]
  },
  { "day":16,"topic":"Algebra","subtopic":"Algebraic Fractions","level":"Higher",
    "block":"Algebra","color":"#2E7D32",
    "concept":{"explain":["Algebraic fractions follow the SAME rules as number fractions. ADD/SUBTRACT: find LCD, convert, combine. SIMPLIFY: factorise top and bottom, cancel common factors. SOLVE: multiply by LCD to clear fractions.","Always check for values making denominators zero (excluded from domain)."],"analogy":"(x²−4)/(x+2) simplifies just like 8/4=2. Factorise numerator: (x+2)(x−2). Cancel (x+2) top and bottom → (x−2). Same logic as number arithmetic, just with expressions.","worked":{"title":"Simplify (x²+5x+6)/(x²−4)","steps":["Factorise top: (x+2)(x+3)","Factorise bottom: (x+2)(x−2)  [DoTS]","Cancel (x+2): result is (x+3)/(x−2)","Restriction: x≠2 and x≠−2"]},"mistakes":["Cancel FACTORS only (things that multiply), not TERMS (things that add)","Factorise denominators FIRST before finding LCD","After clearing fractions: check solution doesn't make any denominator zero"],"formulae":["LCD: factorise denominators, take highest powers","Simplify: factorise → cancel","Solve: multiply by LCD → clear fractions"]},
    "questions":[
      {"q":1,"marks":3,"text":"Simplify: (x+1)/3 + (x−2)/2","answer":"LCD=6: [2(x+1)+3(x−2)]/6 = (5x−4)/6","hint":"Find the LCD (6), convert each fraction, then add numerators."},
      {"q":2,"marks":3,"text":"Write as a single fraction: 1/x + 1/(x+2)","answer":"[(x+2)+x]/[x(x+2)] = (2x+2)/(x²+2x)","hint":"LCD=x(x+2). Multiply each fraction to get this denominator."},
      {"q":3,"marks":4,"text":"Simplify: (x²−4)/(x+2)","answer":"(x+2)(x−2)/(x+2) = x−2  (x≠−2)","hint":"Factorise x²−4 using the Difference of Two Squares."},
      {"q":4,"marks":4,"text":"Simplify: (x²+5x+6)/(x²−4)","answer":"(x+2)(x+3)/[(x+2)(x−2)] = (x+3)/(x−2)","hint":"Factorise both numerator and denominator fully, then cancel."},
      {"q":5,"marks":5,"text":"Express as a single fraction: 3/(x+1) + 2/(x−1)","answer":"[3(x−1)+2(x+1)]/[(x+1)(x−1)] = (5x+1)/(x²−1)","hint":"LCD=(x+1)(x−1). Multiply each numerator accordingly."},
      {"q":6,"marks":5,"text":"Solve: 3/(x−2) + 2 = 5","answer":"3+2(x−2)=5(x−2) → 9=3x → x=3","hint":"Multiply every term by (x−2) to clear the fraction."},
    ]
  },
  { "day":17,"topic":"Algebra Review","subtopic":"Exam-Style Mixed Algebra","level":"Mixed",
    "block":"Algebra","color":"#2E7D32",
    "concept":{"explain":["SEC exam presents algebra as multi-part questions (a)(b)(c) building progressively. 'Hence' means USE your previous answer — faster and shows mathematical connections.","Read ALL parts before starting (a). Later parts reveal what method part (a) should use."],"analogy":"Multi-part questions are like building a bridge: (a) lays the foundation; (b) builds the span; (c) crosses the bridge. Each part makes the next one possible.","worked":{"title":"Strategy: (a) Expand (x−3)(x+5). (b) Hence solve x²+2x−15=0.","steps":["(a) Expand: x²+5x−3x−15=x²+2x−15","(b) HENCE: x²+2x−15=0 → (x−3)(x+5)=0","x=3 or x=−5"]},"mistakes":["Never skip part (a) — later parts say 'hence' and need it","'Hence or otherwise': use 'hence' route, it's faster","Always show formula/method name at each part start"],"formulae":["Read ALL parts before starting","'Hence' = use exact result from previous part","Check: substitute solutions back in"]},
    "questions":[
      {"q":1,"marks":5,"text":"(a) Solve 4x−3=2x+9. (b) Expand (x+2)(x−5). (c) Hence solve x²−3x−10=0.","answer":"(a)x=6. (b)x²−3x−10. (c)(x−5)(x+2)=0→x=5 or x=−2","hint":"Part (c) says 'hence' — use your expansion from (b)!"},
      {"q":2,"marks":5,"text":"f(x)=3x²−2x+1. (a) Find f(2). (b) Solve f(x)=10 (to 1 d.p.). (c) Find the minimum value of f(x).","answer":"(a)9. (b)x≈2.0 or −1.3. (c)min at x=1/3; f(1/3)=2/3","hint":"For (b) set 3x²−2x+1=10, rearrange to =0, use quadratic formula."},
      {"q":3,"marks":5,"text":"Sequence 5,8,11,14,… (a) Find Tₙ. (b) Find T₂₀. (c) Is 200 in the sequence?","answer":"(a)Tₙ=3n+2. (b)T₂₀=62. (c)3n+2=200→n=66. Yes, 200 is 66th term.","hint":"For (c) set Tₙ=200 and solve for n. Check if n is a whole number."},
      {"q":4,"marks":5,"text":"3 adults + 2 children = €40. 2 adults + 4 children = €38. Find adult and child prices.","answer":"3a+2c=40; 2a+4c=38. (i)×2: 6a+4c=80. Subtract: 4a=42→a=€10.50; c=€4.25","hint":"Write two equations, then use elimination."},
      {"q":5,"marks":5,"text":"S=ut+½at². Object falls from rest (u=0), a=10 m/s². How long to fall 150m?","answer":"150=5t²→t²=30→t=√30≈5.48 seconds","hint":"Substitute u=0, a=10, S=150 and solve for t."},
      {"q":6,"marks":5,"text":"(a) Write 2/(x+3)+1/(x−1) as single fraction. (b) Hence solve it=1 (to 2 d.p.).","answer":"(a)(3x+1)/(x²+2x−3). (b)x²−x−4=0→x≈2.56 or −1.56","hint":"For (b) set your single fraction equal to 1 and cross-multiply."},
    ]
  },
  { "day":18,"topic":"Geometry","subtopic":"Lines, Angles & Triangles","level":"Foundation",
    "block":"Geometry","color":"#B8860B",
    "concept":{"explain":["Straight line=180°. Full turn=360°. Vertically opposite angles are EQUAL.","Triangle angles sum 180°. Exterior angle=sum of TWO opposite interior angles. Types: equilateral (3×60°), isosceles (2 equal sides, 2 equal angles), scalene (all different).","Parallel lines: alternate angles (Z)=equal; corresponding angles (F)=equal; co-interior angles (C)=180°."],"analogy":"Angles on a straight line summing to 180° is like sharing a pizza cut on a straight line — all slices on one side must together make a half-circle.","worked":{"title":"Parallel lines, transversal: (3x+10)° and (5x−30)°. Find x.","steps":["Alternate angles (Z): must be equal","3x+10=5x−30","40=2x → x=20","Angle=70°"]},"mistakes":["Exterior angle=sum of OPPOSITE interior angles, NOT adjacent ones","Vertically opposite=EQUAL, not supplementary","Isosceles: only BASE ANGLES are equal"],"formulae":["Triangle: A+B+C=180°","Exterior angle=sum of 2 opposite interior angles","Parallel lines: Z-angles equal; C-angles=180°"]},
    "questions":[
      {"q":1,"marks":2,"text":"A triangle has angles 55°, 70° and x°. Find x.","answer":"x=180−55−70=55°","hint":"Angles in a triangle sum to 180°."},
      {"q":2,"marks":2,"text":"Is the triangle from Q1 equilateral, isosceles or scalene?","answer":"Isosceles: two angles are equal (55°), so two sides are equal.","hint":"Two equal angles means two equal sides."},
      {"q":3,"marks":3,"text":"A triangle has interior angles 45° and 80°. Find the exterior angle at the third vertex.","answer":"Exterior angle=45+80=125°","hint":"Exterior angle = sum of the TWO non-adjacent interior angles."},
      {"q":4,"marks":3,"text":"Two straight lines cross. Vertically opposite angles are (2x+10)° and (3x−20)°. Find x.","answer":"2x+10=3x−20 → x=30°","hint":"Vertically opposite angles are equal — set them equal and solve."},
      {"q":5,"marks":4,"text":"Three angles on a straight line: (4y+10)°, (2y+5)° and 3y°. Find y.","answer":"9y+15=180 → y=165/9≈18.3°","hint":"Angles on a straight line sum to 180°."},
      {"q":6,"marks":4,"text":"A quadrilateral has angles 90°, 85°, 110° and x°. Find x.","answer":"x=360−90−85−110=75°","hint":"Sum of angles in any quadrilateral = 360°."},
    ]
  },
  { "day":19,"topic":"Geometry","subtopic":"Theorems & Proofs","level":"Ordinary",
    "block":"Geometry","color":"#B8860B",
    "concept":{"explain":["Theorem 2: Triangle angles=180°. Theorem 3: Exterior angle=sum of 2 opposite interior angles. Theorem 6 (circle): Angle at centre=2×angle at circumference (same arc). Corollary: Angle in semicircle=90°.","A PROOF: every step justified by a named theorem, axiom or definition."],"analogy":"Theorems are mathematical laws — always true. A proof is a legal argument: you must CITE the law (theorem) that justifies each step, not just assert things are true.","worked":{"title":"O is centre, ∠AOB=120°. Find ∠ACB (C on major arc).","steps":["State: 'By Theorem 6, angle at centre=2×angle at circumference'","120=2×∠ACB","∠ACB=60°"]},"mistakes":["EVERY step in a proof needs a justification — write the theorem name","Theorem 6: angle at centre and angle at circumference must subtend the SAME arc","Angle in semicircle=90° ONLY when chord is a DIAMETER"],"formulae":["Thm 2: A+B+C=180°","Thm 3: Exterior=opposite interior angles","Thm 6: ∠centre=2×∠circumference","Corollary: angle in semicircle=90°"]},
    "questions":[
      {"q":1,"marks":3,"text":"State Theorem 2. Triangle has ∠A=70°, ∠B=∠C. Find ∠B.","answer":"Thm 2: angles sum 180°. 70+2∠B=180 → ∠B=55°","hint":"State the theorem first, then use it to find the unknown angle."},
      {"q":2,"marks":3,"text":"Triangle PQR: ∠P=40°, ∠Q=65°. Find the exterior angle at R.","answer":"By Thm 3: exterior=40+65=105°","hint":"State Theorem 3, then add the two opposite interior angles."},
      {"q":3,"marks":4,"text":"O is centre of circle. ∠ACB=35° (angle at circumference). Find ∠AOB.","answer":"By Thm 6: ∠AOB=2×35°=70°","hint":"Angle at centre = 2 × angle at circumference (same arc)."},
      {"q":4,"marks":4,"text":"PQ is a diameter of a circle. R is a point on the circumference. Find ∠PRQ. Justify.","answer":"By Corollary (angle in semicircle): ∠PRQ=90°","hint":"What happens to the angle at the circumference when the chord is a diameter?"},
      {"q":5,"marks":5,"text":"Circle: O is centre. Chord AB. Prove ∠AOB=2∠ACB where C is on the major arc.","answer":"Join CO, extend to D. OA=OC=OB (radii). △OAC isosceles: ∠OAC=∠OCA=x. Ext ∠AOD=2x. Similarly ∠BOD=2y. ∠AOB=2(x+y)=2∠ACB ✓","hint":"Join CO and extend to a point D on the circle. Use isosceles triangle properties."},
      {"q":6,"marks":5,"text":"ABCD is a parallelogram. Prove ∠DAB=∠BCD using angle theorems.","answer":"AB∥DC → co-int angles: ∠DAB+∠ADC=180°. Also AB∥DC → ∠ABC+∠BCD=180°. So ∠DAB=∠BCD. ✓","hint":"Use the co-interior angles theorem for parallel lines."},
    ]
  },
  { "day":20,"topic":"Geometry","subtopic":"Constructions","level":"Ordinary",
    "block":"Geometry","color":"#B8860B",
    "concept":{"explain":["Key constructions: (1) Perpendicular bisector of a segment. (2) Angle bisector. (3) SSS triangle. (4) SAS triangle. (5) Circumcircle (intersection of perp. bisectors). (6) Incircle (intersection of angle bisectors).","NEVER erase construction arcs in the exam — they prove your method."],"analogy":"The perpendicular bisector finds all points EQUIDISTANT from both endpoints. Compass arcs measure equal distances from each end — their crossings are the equidistant points.","worked":{"title":"Construct perpendicular bisector of AB=8cm","steps":["Draw AB=8cm","Set compass to more than 4cm","Arcs from A above and below AB","SAME compass setting: arcs from B crossing the first arcs","Connect the two intersection points","This line is the perpendicular bisector"]},"mistakes":["Always use compass — not a ruler to mark the midpoint alone","Keep compass width THE SAME for both arcs","NEVER erase arcs — they show your method"],"formulae":["Circumcentre: intersection of perp. bisectors of sides","Incentre: intersection of angle bisectors","SSS: compass arcs from both ends","SAS: protractor for angle, compass for side lengths"]},
    "questions":[
      {"q":1,"marks":3,"text":"Describe step-by-step how to construct the perpendicular bisector of AB=8cm.","answer":"1.Draw AB=8cm. 2.Compass>4cm, arcs from A. 3.Same setting, arcs from B. 4.Connect intersections.","hint":"You need your compass to draw arcs of equal radius from both endpoints."},
      {"q":2,"marks":3,"text":"Describe how to bisect a 60° angle using compass and ruler only.","answer":"1.Arc from vertex. 2.Equal arcs from each crossing. 3.Line from vertex through intersection.","hint":"The bisector of an angle is found by creating two equal-radius arcs."},
      {"q":3,"marks":4,"text":"Describe steps to construct triangle ABC: AB=5cm, BC=7cm, AC=6cm. (SSS)","answer":"1.Draw BC=7cm. 2.Compass 5cm, arc from B. 3.Compass 6cm, arc from C. 4.Intersection=A.","hint":"Draw the base, then swing arcs of the correct length from each endpoint."},
      {"q":4,"marks":4,"text":"Describe constructing triangle: AB=8cm, AC=6cm, ∠BAC=50°. (SAS)","answer":"1.Draw AB=8cm. 2.Measure 50° at A. 3.Mark AC=6cm. 4.Connect BC.","hint":"Draw one side, use a protractor for the angle, mark the second side along that ray."},
      {"q":5,"marks":4,"text":"Explain how to construct the circumscribed circle of a triangle.","answer":"1.Perp bisector of two sides. 2.Intersection=circumcentre. 3.Radius=distance to vertex. 4.Draw circle.","hint":"The circumcentre is equidistant from all three vertices."},
      {"q":6,"marks":5,"text":"Explain how to construct the inscribed circle of a triangle.","answer":"1.Bisect all three angles. 2.Intersection=incentre. 3.Perp from incentre to any side=radius. 4.Draw circle.","hint":"The incentre is equidistant from all three sides."},
    ]
  },
  { "day":21,"topic":"Geometry","subtopic":"Area & Perimeter of 2D Shapes","level":"Foundation→Ordinary",
    "block":"Geometry","color":"#B8860B",
    "concept":{"explain":["PERIMETER=distance around outside (linear units: cm, m). AREA=space covered (square units: cm², m²).","Sector: fraction of full circle. Sector area=(θ/360)×πr². Arc length=(θ/360)×2πr. Perimeter of sector=arc+2 radii.","All formulae are in the Tables booklet — know WHICH to choose and HOW to use it."],"analogy":"Area is how much paint you need to cover a surface. Perimeter is how much frame goes around the edge. 'How much carpet?'=area. 'How much fencing?'=perimeter.","worked":{"title":"Sector: r=9cm, angle=80°. Find area, arc and perimeter.","steps":["Fraction: 80/360=2/9","Area: (2/9)×81π=18π≈56.55 cm²","Arc: (2/9)×18π=4π≈12.57 cm","Perimeter: arc+2r=4π+18≈30.57 cm"]},"mistakes":["Triangle area=½×base×HEIGHT (perpendicular height, not slant!)","Always include units: cm² for area, cm for perimeter","Sector perimeter=arc+TWO radii"],"formulae":["Triangle: A=½bh","Circle: A=πr²; C=2πr","Trapezium: A=½(a+b)h","Sector: A=(θ/360)πr²; Arc=(θ/360)2πr"]},
    "questions":[
      {"q":1,"marks":2,"text":"Find the area of a triangle with base 10cm and height 6cm.","answer":"A=½×10×6=30 cm²","hint":"A=½×base×height (perpendicular height)."},
      {"q":2,"marks":3,"text":"Find area and circumference of a circle radius 7cm.","answer":"A=49π≈153.94 cm²; C=14π≈43.98 cm","hint":"A=πr² and C=2πr with r=7."},
      {"q":3,"marks":3,"text":"Trapezium: parallel sides 5cm and 9cm, height 4cm. Find area.","answer":"A=½(5+9)×4=28 cm²","hint":"A=½(a+b)×h where a and b are the parallel sides."},
      {"q":4,"marks":4,"text":"Sector: radius 8cm, angle 120°. Find area and arc length.","answer":"Area=(120/360)×64π=64π/3≈67.02 cm²; Arc=(120/360)×16π≈16.76 cm","hint":"Calculate the fraction of the full circle first (120/360=1/3)."},
      {"q":5,"marks":4,"text":"Rectangle 12cm×10cm with circle radius 4cm removed. Find shaded area.","answer":"Rectangle=120; Circle=16π≈50.27; Shaded≈69.73 cm²","hint":"Shaded area = total area − area of removed circle."},
      {"q":6,"marks":5,"text":"Sector: radius 10cm, angle 80°. Find the perimeter of the sector.","answer":"Arc=(80/360)×20π=40π/9≈13.96; Perimeter=13.96+20≈33.96 cm","hint":"Perimeter of sector = arc length + 2 radii."},
    ]
  },
  { "day":22,"topic":"Geometry","subtopic":"Volume & Surface Area of 3D Solids","level":"Ordinary",
    "block":"Geometry","color":"#B8860B",
    "concept":{"explain":["VOLUME=space inside (cm³). SURFACE AREA=total area of all faces (cm²). All formulae in Tables booklet.","COMPOSITE SOLID: calculate each part separately, then ADD volumes."],"analogy":"Volume is filling a container with water. Surface area is wrapping a gift — how much paper to cover every face? Completely different measurements needing different formulae.","worked":{"title":"Cone (r=5cm, h=12cm) on hemisphere (r=5cm). Total volume.","steps":["Cone: V=⅓π(25)(12)=100π cm³","Hemisphere: V=(2/3)π(125)=(250π/3) cm³","Total: 100π+(250/3)π=(550/3)π≈576 cm³"]},"mistakes":["Cylinder curved SA=2πrh. Total SA=2πrh+2πr²","Cone slant height: l=√(r²+h²), NOT vertical height","Sphere: V=(4/3)πr³ — students forget the 4/3"],"formulae":["Cuboid: V=lwh; SA=2(lw+lh+wh)","Cylinder: V=πr²h; SA=2πr²+2πrh","Cone: V=⅓πr²h; l=√(r²+h²); SA=πrl+πr²","Sphere: V=(4/3)πr³; SA=4πr²"]},
    "questions":[
      {"q":1,"marks":2,"text":"Find V and SA of a cuboid: 8cm×5cm×3cm.","answer":"V=120 cm³; SA=2(40+24+15)=158 cm²","hint":"V=l×w×h. SA=2(lw+lh+wh)."},
      {"q":2,"marks":3,"text":"Cylinder: radius 4cm, height 10cm. Find V and curved SA.","answer":"V=160π≈502.65 cm³; Curved SA=80π≈251.33 cm²","hint":"V=πr²h; Curved SA=2πrh (no ends)."},
      {"q":3,"marks":3,"text":"Cone: base radius 6cm, height 8cm. Find slant height and total SA.","answer":"l=√(36+64)=10cm; Total SA=96π≈301.6 cm²","hint":"l=√(r²+h²). Total SA=πrl+πr²."},
      {"q":4,"marks":4,"text":"Sphere radius 5cm. Find V and SA.","answer":"V=500π/3≈523.6 cm³; SA=100π≈314.2 cm²","hint":"V=(4/3)πr³; SA=4πr²."},
      {"q":5,"marks":4,"text":"Cone (r=3cm, h=4cm) on hemisphere (r=3cm). Total volume.","answer":"Cone=12π; Hemisphere=18π; Total=30π≈94.25 cm³","hint":"Calculate each part separately using their respective formulae."},
      {"q":6,"marks":5,"text":"Cylinder V=4000cm³, height=twice the radius. Find r and h (to 2 d.p.).","answer":"πr²(2r)=4000→r³=2000/π→r≈8.60cm; h≈17.20cm","hint":"Write h=2r, substitute into V=πr²h and solve for r."},
    ]
  },
  { "day":23,"topic":"Coordinate Geometry","subtopic":"Distance, Midpoint & Slope","level":"Ordinary",
    "block":"Geometry","color":"#B8860B",
    "concept":{"explain":["Distance: |AB|=√[(x₂−x₁)²+(y₂−y₁)²]. Midpoint: M=((x₁+x₂)/2,(y₁+y₂)/2). Slope: m=(y₂−y₁)/(x₂−x₁).","PARALLEL: equal slopes. PERPENDICULAR: m₁×m₂=−1 (negative reciprocal, m⊥=−1/m)."],"analogy":"Slope is like a hill's steepness: slope=3 means 3 steps up for every 1 right. Negative slope=downhill. Two parallel roads have equal steepness; perpendicular roads make perfect right angles.","worked":{"title":"A(1,2) B(7,6). Find slope, length, midpoint, perpendicular slope.","steps":["Slope: (6−2)/(7−1)=4/6=2/3","Length: √[36+16]=√52=2√13","Midpoint: (4,4)","Perp slope: −3/2"]},"mistakes":["Distance: SQUARE the differences — don't just add |Δx|+|Δy|","Slope must be (y₂−y₁)/(x₂−x₁) — mixing up x and y gives wrong answer","Perp slope: flip fraction AND change sign. 2/3 → −3/2"],"formulae":["|AB|=√[(x₂−x₁)²+(y₂−y₁)²]","M=((x₁+x₂)/2,(y₁+y₂)/2)","m=(y₂−y₁)/(x₂−x₁); m⊥=−1/m"]},
    "questions":[
      {"q":1,"marks":3,"text":"Find the distance between A(1,3) and B(5,7).","answer":"|AB|=√[16+16]=√32=4√2≈5.66 units","hint":"Apply the distance formula: √[(x₂−x₁)²+(y₂−y₁)²]."},
      {"q":2,"marks":2,"text":"Find the midpoint of A(1,3) and B(5,7).","answer":"M=((1+5)/2,(3+7)/2)=(3,5)","hint":"Average the x-coordinates and average the y-coordinates."},
      {"q":3,"marks":3,"text":"Find the slope of the line through A(1,3) and B(5,7).","answer":"m=(7−3)/(5−1)=4/4=1","hint":"Slope = rise ÷ run = (y₂−y₁)/(x₂−x₁)."},
      {"q":4,"marks":3,"text":"Find the equation of the line through midpoint M from Q2, perpendicular to AB.","answer":"Perp slope=−1. Through (3,5): y−5=−1(x−3) → x+y−8=0","hint":"The perpendicular slope is −1/m. Use y−y₁=m(x−x₁)."},
      {"q":5,"marks":4,"text":"Find the equation of the line through (−1,2) with slope 3. Write as ax+by+c=0.","answer":"y−2=3(x+1) → 3x−y+5=0","hint":"Use y−y₁=m(x−x₁) with (x₁,y₁)=(−1,2) and m=3."},
      {"q":6,"marks":5,"text":"Line l: through (1,2) and (4,5). Line k: perpendicular to l through (3,−1). Find k's equation and x-intercept.","answer":"m_l=1; m_k=−1. k: y=−x+2. x-intercept at (2,0)","hint":"Find slope of l, then find perpendicular slope. Use point-slope form for k."},
    ]
  },
  { "day":24,"topic":"Coordinate Geometry","subtopic":"Equation of Line & Circle","level":"Ordinary→Higher",
    "block":"Geometry","color":"#B8860B",
    "concept":{"explain":["Line: y−y₁=m(x−x₁). Rearrange to y=mx+c or ax+by+c=0.","Circle: (x−h)²+(y−k)²=r² with centre (h,k) and radius r.","Point vs circle: distance from centre < r → inside; = r → on circle; > r → outside."],"analogy":"The circle equation is Pythagoras in disguise. Any point on the circle is exactly r units from the centre. Distance formula gives r² on both sides after squaring — that's the circle equation.","worked":{"title":"Circle diameter endpoints (−2,3) and (4,7). Find equation.","steps":["Centre=midpoint=((−2+4)/2,(3+7)/2)=(1,5)","r=½√[(4+2)²+(7−3)²]=½√52=√13","Equation: (x−1)²+(y−5)²=13"]},"mistakes":["Line: for point (3,−2) → y−(−2)=m(x−3) → y+2=m(x−3). Note double negative!","Circle: r is radius. If r=5, write =25 (which is r²), not =5","To find where circle crosses axes: set y=0 or x=0"],"formulae":["Line: y−y₁=m(x−x₁)","Circle: (x−h)²+(y−k)²=r²","Diameter→centre=midpoint; r=½diameter length"]},
    "questions":[
      {"q":1,"marks":2,"text":"Find slope and intercepts of y=2x+3.","answer":"Slope=2; y-int=(0,3); x-int=(−3/2,0)","hint":"At y-intercept, x=0. At x-intercept, y=0."},
      {"q":2,"marks":3,"text":"Find intersection of 2x+y=7 and x−2y=1.","answer":"y=7−2x; sub: x−14+4x=1→x=3,y=1. Point (3,1)","hint":"Substitute one equation into the other (substitution method)."},
      {"q":3,"marks":3,"text":"Write equation of circle: centre (2,−3), radius 5.","answer":"(x−2)²+(y+3)²=25","hint":"Use (x−h)²+(y−k)²=r² with h=2, k=−3, r=5."},
      {"q":4,"marks":4,"text":"Circle x²+y²=25. Find where it crosses axes. State centre and radius.","answer":"Centre (0,0), r=5. x-axis: (±5,0). y-axis: (0,±5)","hint":"Set y=0 for x-axis crossings; set x=0 for y-axis crossings."},
      {"q":5,"marks":4,"text":"Circle (x−3)²+(y+1)²=16. Centre, radius. Is (7,−1) on circle?","answer":"Centre (3,−1), r=4. Check (7,−1): (4)²+(0)²=16 ✓ On circle","hint":"Substitute the point into the circle equation. If LHS=r², it's on the circle."},
      {"q":6,"marks":5,"text":"Circle with diameter endpoints (−2,1) and (4,7). Find centre, radius and equation.","answer":"Centre=(1,4); r=3√2; Equation:(x−1)²+(y−4)²=18","hint":"Centre=midpoint of diameter. Radius=half the diameter length."},
    ]
  },
  { "day":25,"topic":"Trigonometry","subtopic":"SOH CAH TOA — Right-Angled Triangles","level":"Ordinary",
    "block":"Geometry","color":"#B8860B",
    "concept":{"explain":["sinθ=O/H; cosθ=A/H; tanθ=O/A. Hypotenuse=always opposite right angle. Opposite and adjacent are defined relative to the angle you are working with.","To find a side: set up the ratio, solve. To find an angle: use sin⁻¹, cos⁻¹, or tan⁻¹.","Pythagoras: a²+b²=c² (right triangles only, c=hypotenuse)."],"analogy":"SOH CAH TOA is a tour guide at your working angle. Looking from there: the side opposite is OPPOSITE; the side next to the guide (not hypotenuse) is ADJACENT; the longest side across from the right angle is HYPOTENUSE.","worked":{"title":"8m ladder, base 3m from wall. Find angle with ground.","steps":["cosθ=adjacent/hypotenuse=3/8","θ=cos⁻¹(3/8)≈68.0°","Check: sin68°≈0.927; opp=8×0.927≈7.42m; 3²+7.42²≈64=8² ✓"]},"mistakes":["ALWAYS draw a diagram first. Label O, A, H relative to the GIVEN angle","Hypotenuse is opposite the RIGHT ANGLE, not your working angle","Calculator must be in DEGREE mode, not radians"],"formulae":["sinθ=O/H  cosθ=A/H  tanθ=O/A","Pythagoras: a²+b²=c²","θ=sin⁻¹(x), cos⁻¹(x), tan⁻¹(x)"]},
    "questions":[
      {"q":1,"marks":2,"text":"Right triangle: hypotenuse 13cm, one leg 5cm. Find the other leg.","answer":"a²=13²−5²=144 → a=12 cm","hint":"Pythagoras: a²+b²=c². Rearrange to find a."},
      {"q":2,"marks":3,"text":"Right triangle: hypotenuse 7cm, angle 40°. Find side opposite to 40°.","answer":"sin40°=opp/7 → opp=7×0.6428≈4.50 cm","hint":"Which ratio uses Opposite and Hypotenuse? SOH: sinθ=O/H."},
      {"q":3,"marks":3,"text":"Right triangle: legs 6cm and 8cm. Find angle opposite the 8cm leg.","answer":"tanθ=8/6 → θ=tan⁻¹(1.333)≈53.1°","hint":"Which ratio uses Opposite and Adjacent? TOA: tanθ=O/A."},
      {"q":4,"marks":4,"text":"12m ladder makes 25° with the wall. How far is the base from the wall?","answer":"cos25°=adj/12 → adj=12×cos25°≈10.88m","hint":"Draw a diagram. The angle is with the WALL — label sides accordingly."},
      {"q":5,"marks":4,"text":"Person 40m from a 30m building. Find angle of elevation to the top.","answer":"tanθ=30/40 → θ=tan⁻¹(0.75)≈36.9°","hint":"Draw a right triangle. The 40m is adjacent and 30m is opposite."},
      {"q":6,"marks":5,"text":"From A, angle of elevation=35°. From B (50m further), angle=20°. Find tower height.","answer":"h=x·tan35°=(x+50)tan20°. x(tan35−tan20)=50tan20 → h≈37.9m","hint":"Set up two equations using tan from each point, then solve simultaneously."},
    ]
  },
  { "day":26,"topic":"Trigonometry","subtopic":"Sine Rule, Cosine Rule & Area","level":"Higher",
    "block":"Geometry","color":"#B8860B",
    "concept":{"explain":["SINE RULE: a/sinA=b/sinB=c/sinC. Use for AAS, ASA.","COSINE RULE: a²=b²+c²−2bc cosA. Use for SAS (find side) or SSS (find angle). Rearranged: cosA=(b²+c²−a²)/2bc.","AREA of any triangle: ½ab sinC (C is angle BETWEEN sides a and b). All in Tables booklet."],"analogy":"Sine Rule: works when you have an angle opposite a known side. Cosine Rule: works when you're 'stuck' with two sides around an angle (SAS) or all three sides (SSS).","worked":{"title":"PQ=7, PR=5, ∠QPR=60°. Find QR and area.","steps":["SAS → Cosine Rule","QR²=49+25−70(0.5)=39","QR=√39≈6.24cm","Area=½×7×5×sin60°≈15.16 cm²"]},"mistakes":["Cosine Rule: angle A must be OPPOSITE the side a you're finding","Finding angle from Cosine Rule: cosA=(b²+c²−a²)/2bc → use cos⁻¹","Area: angle must be BETWEEN the two sides used"],"formulae":["Sine Rule: a/sinA=b/sinB=c/sinC","Cosine Rule: a²=b²+c²−2bc cosA","Area: ½ab sinC"]},
    "questions":[
      {"q":1,"marks":3,"text":"Triangle: ∠A=40°, ∠B=70°, b=8cm. Find a using Sine Rule.","answer":"a/sin40=8/sin70 → a=8sin40/sin70≈5.47 cm","hint":"Find the missing angle C first, then apply the Sine Rule."},
      {"q":2,"marks":3,"text":"Triangle from Q1: find side c.","answer":"∠C=70°; c/sin70=8/sin70 → c=8 cm (isosceles)","hint":"∠C=180−40−70=70°. Apply Sine Rule."},
      {"q":3,"marks":4,"text":"Triangle: PQ=7cm, PR=5cm, ∠QPR=60°. Find QR using Cosine Rule.","answer":"QR²=49+25−70cos60=39 → QR=√39≈6.24cm","hint":"SAS: use Cosine Rule a²=b²+c²−2bc cosA where A=60°."},
      {"q":4,"marks":4,"text":"Find the area of triangle from Q3.","answer":"Area=½×7×5×sin60°=35√3/4≈15.16 cm²","hint":"Area=½ab sinC where C is the INCLUDED angle."},
      {"q":5,"marks":5,"text":"Triangle sides: a=7, b=6, c=5. Find angle A using Cosine Rule.","answer":"cosA=(36+25−49)/60=0.2 → A=cos⁻¹(0.2)≈78.5°","hint":"Rearrange Cosine Rule: cosA=(b²+c²−a²)/(2bc)."},
      {"q":6,"marks":5,"text":"Ship sails 12km on bearing 040°, then 15km on bearing 150°. Distance from start? (Angle between paths=110°)","answer":"d²=144+225−360cos110≈492.1 → d≈22.2km","hint":"The angle between the two paths is 110°. Apply the Cosine Rule."},
    ]
  },
  { "day":27,"topic":"Geometry","subtopic":"Mixed Problem Solving","level":"Mixed",
    "block":"Geometry","color":"#B8860B",
    "concept":{"explain":["Multi-step geometry: SEQUENCE different skills. Write each formula and sub-result clearly on its own line. Wrong early value? Examiners still give method marks for correct process in later steps."],"analogy":"A relay race: each runner (step) carries the baton (answer) to the next. Even if one runner makes an error, the next can still complete their section — examiners follow YOUR numbers through subsequent steps.","worked":{"title":"Isosceles triangle: base 16cm, equal sides 10cm. Area and perimeter.","steps":["Drop perpendicular from apex — bisects base: 8cm + 8cm","Pythagoras: h²=10²−8²=36 → h=6cm","Area=½×16×6=48 cm²","Perimeter=16+10+10=36 cm"]},"mistakes":["Composite solids: calculate each part separately, then ADD","Angle of elevation: measured from the HORIZONTAL","When asked 'hence', use your PREVIOUS answer"],"formulae":["Multi-step: identify→formula→substitute→evaluate","Composite: V_total=V₁+V₂","Consequential marks apply if you carry forward wrong values"]},
    "questions":[
      {"q":1,"marks":5,"text":"Isosceles triangle: base 12cm, equal sides 10cm. Find area and perimeter.","answer":"h=√(100−36)=8cm. Area=48 cm². Perimeter=32 cm","hint":"Drop a perpendicular from the apex to find the height first."},
      {"q":2,"marks":5,"text":"Swimming pool: trapezoidal cross-section (widths 6m and 10m, depth 4m), length 20m. Find volume.","answer":"Cross-section=½(6+10)×4=32 m². V=32×20=640 m³","hint":"V = area of cross-section × length."},
      {"q":3,"marks":5,"text":"A(1,2), B(5,8). Find: (i)slope, (ii)|AB|, (iii)midpoint, (iv)equation of perpendicular bisector.","answer":"(i)3/2. (ii)2√13. (iii)(3,5). (iv)2x+3y=21","hint":"Find each in order — the perpendicular bisector goes through the midpoint with perpendicular slope."},
      {"q":4,"marks":5,"text":"Wire 50m makes 32° with ground. Find mast height. From 60m from base, find angle of elevation.","answer":"h=50sin32°≈26.5m. tanα=26.5/60→α≈23.8°","hint":"Use sinθ=O/H for the first part, then tanθ=O/A for the second."},
      {"q":5,"marks":5,"text":"Equilateral triangle, area 36√3 cm². Find side length, perimeter and inscribed circle radius.","answer":"√3/4×s²=36√3→s=12cm. P=36cm. r=2√3≈3.46cm","hint":"Area of equilateral triangle=√3/4×s². Then find r=s/(2√3)."},
      {"q":6,"marks":5,"text":"Cone: height=3×radius, volume=1000π cm³. Find r, h, slant height, lateral SA.","answer":"πr³=1000π→r=10cm; h=30cm; l=10√10≈31.6cm; LSA≈994 cm²","hint":"Substitute h=3r into V=⅓πr²h and solve for r."},
    ]
  },
  { "day":28,"topic":"Coordinate Geometry","subtopic":"Exam-Style Mixed Practice","level":"Higher",
    "block":"Geometry","color":"#B8860B",
    "concept":{"explain":["Full exam-style coordinate geometry. Difficulty: (a)slope/distance; (b)equation of line or circle; (c)intersection or point vs circle.","Key: perp bisector of a chord passes through the CENTRE. Circle from diameter → centre=midpoint of diameter."],"analogy":"Coordinate geometry questions are a treasure map: (a) gives direction (slope); (b) gives the path (equation); (c) finds where the path leads (intersection, inside/outside circle).","worked":{"title":"A(−1,3) B(5,7). Find perp bisector. Verify it passes through midpoint.","steps":["Mid M=(2,5); slope AB=2/3","Perp slope=−3/2","Equation: y−5=−3/2(x−2) → 3x+2y=16","Verify M(2,5): 3(2)+2(5)=16 ✓"]},"mistakes":["Perp bisector: MUST pass through midpoint AND have perpendicular slope","Distance from centre to point: use distance formula, not circle equation","x-intercept: set y=0; y-intercept: set x=0"],"formulae":["Perp bisector: through midpoint, slope=−1/m_AB","Outside/on/inside: compare d(centre,point) with r"]},
    "questions":[
      {"q":1,"marks":5,"text":"A(1,1), B(3,5), C(0,4). Eq. of AB. Line through C perpendicular to AB.","answer":"AB: m=2; 2x−y−1=0. Perp through C: m=−1/2; x+2y−8=0","hint":"Find slope of AB, then perpendicular slope=−1/slope of AB."},
      {"q":2,"marks":5,"text":"Find intersection D of line AB and line CD from Q1.","answer":"2x−y=1 and x+2y=8. → x=2, y=3. D=(2,3)","hint":"Solve the two line equations simultaneously."},
      {"q":3,"marks":5,"text":"Find |CD| and midpoint of CD where C=(0,4) and D=(2,3).","answer":"|CD|=√5; midpoint=(1,3.5)","hint":"Apply distance formula and midpoint formula."},
      {"q":4,"marks":5,"text":"Circle: diameter endpoints (−1,1) and (3,5). Find centre, radius and equation.","answer":"Centre=(1,3); r=2√2; Equation:(x−1)²+(y−3)²=8","hint":"Centre=midpoint of diameter. r=half the diameter length."},
      {"q":5,"marks":5,"text":"Using the circle from Q4, find any x-axis and y-axis intercepts.","answer":"No x-intercepts (discriminant<0). y-intercepts: y=3±√7≈5.65 or 0.35","hint":"Set x=0 for y-intercepts; set y=0 for x-intercepts. Check if solutions are real."},
      {"q":6,"marks":5,"text":"Is P(4,3) inside, on, or outside the circle from Q4? Show reasoning.","answer":"Distance from (1,3) to (4,3)=3. r=2√2≈2.83. Since 3>2.83, P is OUTSIDE.","hint":"Calculate distance from centre to P and compare with the radius."},
    ]
  },
  { "day":29,"topic":"Statistics","subtopic":"Data Collection & Frequency Tables","level":"Foundation",
    "block":"Statistics","color":"#6A0572",
    "concept":{"explain":["DISCRETE data: countable (goals, shoes). CONTINUOUS data: measurable, any value in a range (height, time). PRIMARY: you collect it. SECONDARY: already collected.","Frequency table: tally each value. Relative frequency=freq÷total."],"analogy":"Statistics is detective work. Gather evidence (data), sort it (frequency table), look for patterns (analysis), draw conclusions (interpretation). A frequency table sorts evidence into labelled boxes.","worked":{"title":"Shoe sizes: 5,6,5,7,6,6,5,7,8,6. Frequency table.","steps":["Values: 5,6,7,8","Tally: 5→3; 6→4; 7→2; 8→1","Check: 3+4+2+1=10 ✓","Mode=6 (highest frequency)","Relative freq of 6: 4/10=40%"]},"mistakes":["Discrete='countable' (whole numbers only). Continuous='measurable' (any decimal value)","Relative frequency: always 0 to 1. If >1, you divided the wrong way","Tally marks: always in groups of 5 (IIII)"],"formulae":["Relative frequency=freq÷total","Mode=value with highest frequency"]},
    "questions":[
      {"q":1,"marks":2,"text":"Is the number of goals scored in a match discrete or continuous? Explain.","answer":"Discrete: you can only score whole numbers of goals — countable.","hint":"Can the value be any decimal? Or only whole numbers?"},
      {"q":2,"marks":2,"text":"Is the height of students discrete or continuous? Explain.","answer":"Continuous: height can be any value, e.g. 163.7 cm — measurable.","hint":"Can height be 163.7 cm? Then it's continuous."},
      {"q":3,"marks":3,"text":"30 students surveyed: 12 chose blue as favourite colour. Find relative frequency of blue.","answer":"12/30=0.4=40%","hint":"Relative frequency = frequency ÷ total."},
      {"q":4,"marks":3,"text":"Scores: 3,2,4,1,3,2,3,5,4,2,3,1,4,3,5,2,3,4,2,5. Make a frequency table and find the mode.","answer":"1:2, 2:5, 3:7, 4:4, 5:3. Mode=3 (highest frequency, appears 7 times).","hint":"Tally each score carefully. The mode has the highest frequency."},
      {"q":5,"marks":4,"text":"Add a cumulative frequency column to your table from Q4.","answer":"CumFreq: 1→2; 2→7; 3→14; 4→18; 5→21","hint":"Add each frequency to the running total."},
      {"q":6,"marks":4,"text":"Data: 1,2,3,2,3,4,3,2,4,3,1,3,4,2,3,5,3,4,2,3. Find mean using frequency table.","answer":"Freq: 1:2,2:5,3:8,4:4,5:1; Σfx=57; Mean=57/20=2.85","hint":"Mean=Σ(f×x)÷total. Multiply each value by its frequency."},
    ]
  },
  { "day":30,"topic":"Statistics","subtopic":"Mean, Median, Mode, Range & IQR","level":"Ordinary",
    "block":"Statistics","color":"#6A0572",
    "concept":{"explain":["MEAN=sum÷count (affected by outliers). MEDIAN=middle value when ordered (not affected). MODE=most frequent. RANGE=max−min.","QUARTILES: Q1(lower), Q2(median), Q3(upper). IQR=Q3−Q1 (measures spread of middle 50%, more reliable than range)."],"analogy":"Mean is like sharing pizza equally — if one person takes 90% (outlier), the 'fair share' seems inflated. The MEDIAN shows what the typical person actually got — unaffected by the outlier.","worked":{"title":"Data 4,7,9,2,8,11,7,5,12,3. Find mean, median, Q1,Q3,IQR.","steps":["Order: 2,3,4,5,7,7,8,9,11,12","Mean=68/10=6.8","Median=(7+7)/2=7","Q1=median of {2,3,4,5,7}=4","Q3=median of {7,8,9,11,12}=9","IQR=9−4=5"]},"mistakes":["ALWAYS order data before finding median or quartiles","n=10: median=average of 5th and 6th. n=9: median=5th value","IQR=Q3−Q1. NOT Q2−Q1 or Q3−Q2"],"formulae":["Mean=Σx/n","Median: middle value (order first!)","IQR=Q3−Q1","Table: Mean=Σ(f×x)/Σf"]},
    "questions":[
      {"q":1,"marks":2,"text":"Find the median of: 7, 13, 5, 9, 14, 3, 11.","answer":"Ordered: 3,5,7,9,11,13,14. Median=9 (4th value)","hint":"Order the data first! The median is the middle value."},
      {"q":2,"marks":3,"text":"Find mean and range for the data in Q1.","answer":"Mean=(3+5+7+9+11+13+14)/7=62/7≈8.86; Range=14−3=11","hint":"Mean=sum÷count. Range=max−min."},
      {"q":3,"marks":3,"text":"Score freq table: 1(5),2(8),3(12),4(4),5(1). Find mean.","answer":"Σfx=5+16+36+16+5=78. n=30. Mean=78/30=2.6","hint":"Mean=Σ(f×x)÷total. Multiply each score by its frequency."},
      {"q":4,"marks":4,"text":"Ages: 0−10(3), 10−20(8), 20−30(14), 30−40(10), 40−50(5). Estimate mean age.","answer":"Midpoints 5,15,25,35,45. Σfx=1060. n=40. Mean=26.5","hint":"Use midpoints of each group (5,15,25,35,45). Mean=Σ(f×midpoint)÷n."},
      {"q":5,"marks":4,"text":"Class of 12: mean mark 85.6. 13th student joins scoring 91. Find new mean.","answer":"Old sum=1027.2. New sum=1118.2. New mean=1118.2/13≈86.0","hint":"Find the total of the original 12, add the new score, divide by 13."},
      {"q":6,"marks":5,"text":"Find median, Q1, Q3 and IQR for: 5,3,8,2,7,5,9,6,4,10.","answer":"Ordered: 2,3,4,5,5,6,7,8,9,10. Median=5.5. Q1=4. Q3=8. IQR=4","hint":"Order the data, split into two halves, find median of each half for Q1 and Q3."},
    ]
  },
  { "day":31,"topic":"Statistics","subtopic":"Charts & Diagrams","level":"Foundation→Ordinary",
    "block":"Statistics","color":"#6A0572",
    "concept":{"explain":["BAR CHART: gaps between bars, discrete/categorical. HISTOGRAM: no gaps, continuous, y-axis=frequency density=freq÷class width.","PIE CHART: sector angle=(freq÷total)×360°. STEM-AND-LEAF: shows actual data in order; stem=tens digit, leaf=units."],"analogy":"A histogram is like a city skyline — each building (bar) covers a range. A pie chart divides 360° like sharing a round pizza proportionally.","worked":{"title":"Data 14,22,19,31,27,15,23,18,28,11. Stem-and-leaf + median.","steps":["1|1 4 5 8 9","2|2 3 7 8","3|1","Ordered: 11,14,15,18,19,22,23,27,28,31","Median=(19+22)/2=20.5"]},"mistakes":["Histogram y-axis: equal widths→frequency ok; different widths→MUST use frequency density","Pie chart: all angles must SUM to 360°","Bar chart=gaps (discrete); histogram=no gaps (continuous)"],"formulae":["Pie sector=(f/total)×360°","Freq density=freq÷class width"]},
    "questions":[
      {"q":1,"marks":2,"text":"Class votes: A(40),B(30),C(20),D(30). Total=120. Find sector angle for each.","answer":"A:120°, B:90°, C:60°, D:90°. Sum=360° ✓","hint":"Angle=(frequency÷total)×360°."},
      {"q":2,"marks":3,"text":"Draw a stem-and-leaf for: 23,18,35,29,20,15,24,31,27,12.","answer":"1|2 5 8; 2|0 3 4 7 9; 3|1 5","hint":"Stem=tens digit, leaf=units digit. Order the leaves on each stem."},
      {"q":3,"marks":3,"text":"Using your stem-and-leaf from Q2, find the median.","answer":"Ordered: 12,15,18,20,23,24,27,29,31,35 (n=10). Median=(23+24)/2=23.5","hint":"The stem-and-leaf already puts data in order — find the middle value."},
      {"q":4,"marks":4,"text":"Ages: 0−10(6),10−20(14),20−30(20),30−40(8),40−50(2). Find frequency density for each.","answer":"All class widths=10. FD: 0.6, 1.4, 2.0, 0.8, 0.2","hint":"Frequency density=frequency÷class width. All widths are 10 here."},
      {"q":5,"marks":4,"text":"From a histogram, how do you find the number of people in a specific age range?","answer":"Frequency=frequency density×class width. Multiply bar height by class width.","hint":"In a histogram, AREA of bar=frequency."},
      {"q":6,"marks":5,"text":"Using Q4 data (n=50): find modal class and estimate median age.","answer":"Modal class: 20−30 (freq=20). Median=25th value. CumFreq: 6,20,40. Median in 20−30 class. Est≈22.5","hint":"Modal class has highest frequency. Find where the 25th value falls in cumulative frequency."},
    ]
  },
  { "day":32,"topic":"Statistics","subtopic":"Scatter Diagrams & Correlation","level":"Ordinary",
    "block":"Statistics","color":"#6A0572",
    "concept":{"explain":["SCATTER DIAGRAM: plots (x,y) pairs. CORRELATION: positive (both up), negative (one up, other down), none.","LINE OF BEST FIT: must pass through MEAN POINT (x̄,ȳ). INTERPOLATION (within range): reliable. EXTRAPOLATION (outside range): unreliable.","CORRELATION ≠ CAUSATION: a link doesn't mean one causes the other."],"analogy":"Ice cream sales and drownings both increase in summer — strong positive correlation — but ice cream does NOT cause drowning. Both are caused by a third factor: hot weather. Always look for lurking variables!","worked":{"title":"Hours x=(1,2,3,4,5,6). Scores y=(45,55,60,70,75,85). Mean point and correlation.","steps":["x̄=(1+2+3+4+5+6)/6=3.5","ȳ=(45+55+60+70+75+85)/6=65","Mean point: (3.5,65) — line must pass through this","Correlation: strong positive"]},"mistakes":["Line of best fit: NOT always through origin. MUST pass through mean point.","Extrapolation: predicting well beyond data range is very unreliable","Draw line across the WHOLE plot, not just between two specific points"],"formulae":["Mean point: (x̄,ȳ) — line must pass through this","Interpolation: reliable; Extrapolation: unreliable","Correlation ≠ Causation"]},
    "questions":[
      {"q":1,"marks":2,"text":"Scatter plot: study hours on x-axis, marks on y-axis. Points trend upward. Describe correlation.","answer":"Strong positive correlation: as study hours increase, marks tend to increase.","hint":"Does one variable increase as the other increases? That's positive correlation."},
      {"q":2,"marks":2,"text":"Points cluster tightly in a downward-sloping pattern. Describe the correlation.","answer":"Strong negative correlation: as one variable increases, the other decreases closely.","hint":"Downward slope = negative; tight cluster = strong."},
      {"q":3,"marks":3,"text":"Hours: 2,3,4,5,6,7,8. Scores: 55,60,65,70,75,80,85. Calculate mean point (x̄,ȳ).","answer":"x̄=35/7=5; ȳ=490/7=70. Mean point: (5,70)","hint":"The line of best fit MUST pass through the mean point."},
      {"q":4,"marks":4,"text":"Using data from Q3, predict score for 9 hours study (if appropriate).","answer":"Pattern is linear (slope=5 per hour). At x=9, predict y≈90. (Slight extrapolation — caution needed.)","hint":"Draw the line of best fit through (5,70) and extend it to x=9."},
      {"q":5,"marks":4,"text":"A study finds positive correlation between TV hours and exam marks. Does TV cause better results?","answer":"No — correlation ≠ causation. A third variable (motivated student) may cause both.","hint":"Think of what else might explain BOTH variables."},
      {"q":6,"marks":5,"text":"Why would predicting a score for 20 study hours using the Q3 line be unreliable?","answer":"Extrapolation: 20 hours is far outside the data range (2−8). Linear trend may break down; other factors (fatigue, sleep) would dominate.","hint":"What happens when you predict far beyond your data range?"},
    ]
  },
  { "day":33,"topic":"Probability","subtopic":"Basic Probability & Sample Space","level":"Foundation",
    "block":"Statistics","color":"#6A0572",
    "concept":{"explain":["P(A)=favourable outcomes÷total outcomes. Always 0≤P(A)≤1.","COMPLEMENT: P(not A)=1−P(A). SAMPLE SPACE: list of ALL possible outcomes.","MUTUALLY EXCLUSIVE: cannot both occur. P(A or B)=P(A)+P(B)."],"analogy":"Probability is like a weather forecast. 70% chance of rain means: in 100 identical days, expect rain in about 70. P=0 means impossible. P=1 means certain. P=0.5 means equally likely.","worked":{"title":"Die roll. P(prime), P(not prime), P(even or prime).","steps":["Sample space: {1,2,3,4,5,6}","Primes: {2,3,5} → P(prime)=3/6=1/2","P(not prime)=1−1/2=1/2","P(even or prime)=P(E)+P(P)−P(E∩P)=1/2+1/2−1/6=5/6"]},"mistakes":["P(A or B)=P(A)+P(B) ONLY for mutually exclusive events! Otherwise subtract the overlap.","Expected frequency ≠ guaranteed. P=0.3 and 100 days → EXPECT 30, could get more or fewer.","Sample space: list ALL outcomes including those not satisfying the event"],"formulae":["P(A)=favourable÷total","P(not A)=1−P(A)","P(A or B)=P(A)+P(B)−P(A∩B)","Expected freq=P(A)×trials"]},
    "questions":[
      {"q":1,"marks":2,"text":"Bag: 4 red, 5 blue, 3 green. P(picking red)?","answer":"P(red)=4/12=1/3","hint":"P(A)=favourable outcomes÷total outcomes."},
      {"q":2,"marks":2,"text":"Using Q1, find P(not red).","answer":"P(not red)=1−1/3=2/3","hint":"P(not A)=1−P(A)."},
      {"q":3,"marks":3,"text":"List sample space for tossing two coins. Find P(exactly one head).","answer":"Sample space: {HH,HT,TH,TT}. P(one H)=2/4=1/2","hint":"List all 4 combinations systematically."},
      {"q":4,"marks":3,"text":"Fair die rolled. Find P(2 or 5).","answer":"Mutually exclusive: P(2or5)=1/6+1/6=1/3","hint":"Can you get both 2 and 5 in one roll? No → mutually exclusive, just add."},
      {"q":5,"marks":4,"text":"Die rolled. Find P(even), P(prime), P(even or prime). Are even and prime mutually exclusive?","answer":"P(even)=1/2; P(prime)=1/2; NOT mut. exclusive (2 is both); P(even or prime)=5/6","hint":"2 is both even and prime! So they're not mutually exclusive. Subtract the overlap."},
      {"q":6,"marks":4,"text":"Fair die rolled 150 times. How many times expect score > 4?","answer":"P(>4)=P(5or6)=2/6=1/3. Expected=150×1/3=50 times","hint":"Find P(>4) first, then multiply by the number of trials."},
    ]
  },
  { "day":34,"topic":"Probability","subtopic":"Combined Events & Tree Diagrams","level":"Ordinary",
    "block":"Statistics","color":"#6A0572",
    "concept":{"explain":["INDEPENDENT: P(A and B)=P(A)×P(B). DEPENDENT (without replacement): P(A then B)=P(A)×P(B|A).","TREE DIAGRAMS: MULTIPLY along branches (AND). ADD across branches for same outcome (OR). All final branches must SUM to 1."],"analogy":"A tree diagram is like a decision tree. You multiply along a PATH (each branch follows the previous). You ADD across PATHS to find total probability of reaching the same destination.","worked":{"title":"Bag 5R, 7B. Without replacement. P(one red, one blue).","steps":["P(R then B)=(5/12)×(7/11)=35/132","P(B then R)=(7/12)×(5/11)=35/132","P(one of each)=70/132=35/66","Check: all branches sum to 1 ✓"]},"mistakes":["Without replacement: BOTH total AND the selected colour decrease by 1","Tree: multiply ALONG; ADD across for same outcome","Conditional P(A|B): use B row/column total, NOT grand total"],"formulae":["Independent: P(A and B)=P(A)×P(B)","Dependent: P(A then B)=P(A)×P(B|A)","Tree: ×along; +across for same outcome"]},
    "questions":[
      {"q":1,"marks":3,"text":"Bag: 4 red, 8 blue. Two drawn without replacement. P(both red).","answer":"P(RR)=4/12×3/11=12/132=1/11","hint":"Without replacement: second draw has 11 counters, only 3 red."},
      {"q":2,"marks":3,"text":"Using Q1, find P(one red and one blue) in either order.","answer":"P(RB)+P(BR)=(4/12)(8/11)+(8/12)(4/11)=64/132=16/33","hint":"Two orders possible: RB and BR. Add both probabilities."},
      {"q":3,"marks":4,"text":"Draw tree diagram for tossing fair coin twice. Find P(at least one head).","answer":"P(TT)=0.25. P(at least one H)=1−0.25=0.75","hint":"Easiest: P(at least one H)=1−P(no heads)=1−P(TT)."},
      {"q":4,"marks":4,"text":"Class of 40: 25 play sport (8 also do music), 15 do music. Find P(sport and music) and P(sport|music).","answer":"P(S∩M)=8/40=0.2. P(S|M)=8/15","hint":"For conditional P: use the GIVEN condition as your new total (15 students do music)."},
      {"q":5,"marks":5,"text":"Tennis: 60% first serves in, win 70% of those. First fault (40%): 2nd serve in 80%, win 60%. Find P(win point).","answer":"P(win)=0.6×0.7+0.4×0.8×0.6=0.42+0.192=0.612","hint":"Draw a tree. Multiply along each path, then add the paths where the player wins."},
      {"q":6,"marks":5,"text":"Box1: 3R,2B. Box2: 4R,3B. One ball from each. P(same colour).","answer":"P(RR)=(3/5)(4/7)=12/35. P(BB)=(2/5)(3/7)=6/35. P(same)=18/35","hint":"Two ways to get 'same colour': both red OR both blue. Find each and add."},
    ]
  },
  { "day":35,"topic":"Probability","subtopic":"Counting Principles & Expected Value","level":"Higher",
    "block":"Statistics","color":"#6A0572",
    "concept":{"explain":["FUNDAMENTAL COUNTING PRINCIPLE: m ways × n ways = m×n ways. PERMUTATIONS (order matters): nPr=n!/(n−r)! COMBINATIONS (order doesn't matter): nCr=n!/(r!(n−r)!).","EXPECTED VALUE: E(X)=Σ[x×P(x)]. Fair game: E(X)=0."],"analogy":"Permutations=PASSWORDS (ABC≠CAB). Combinations=COMMITTEES (same people, different order = same committee). Use ⁿCᵣ on your calculator!","worked":{"title":"8 people: (a) elect president+sec+treasurer (b) form committee of 3","steps":["(a) ORDER MATTERS: ⁸P₃=8×7×6=336","(b) ORDER DOESN'T MATTER: ⁸C₃=336/6=56"]},"mistakes":["Always ask: does ORDER matter? Yes→Permutation. No→Combination","0!=1 (by definition)","Negative E(X) means expected LOSS"],"formulae":["n!=n×(n−1)×…×1","nPr=n!/(n−r)!  [order matters]","nCr=n!/(r!(n−r)!)  [order doesn't]","E(X)=Σ[x×P(x)]"]},
    "questions":[
      {"q":1,"marks":2,"text":"How many ways can 5 students sit in a row?","answer":"5!=120 ways","hint":"5×4×3×2×1"},
      {"q":2,"marks":3,"text":"Wardrobe: 3 shirts, 2 jumpers, 2 trousers, 2 shoes. How many outfits?","answer":"3×2×2×2=24 outfits","hint":"Fundamental Counting Principle: multiply all choices."},
      {"q":3,"marks":3,"text":"Choose 2 students from 6 (order doesn't matter).","answer":"⁶C₂=15 ways","hint":"⁶C₂=6!/(2!4!)=(6×5)/(2×1)=15"},
      {"q":4,"marks":4,"text":"From 5 candidates: elect president, secretary, treasurer. How many ways?","answer":"⁵P₃=5×4×3=60 ways (order matters — different roles)","hint":"Different roles means order matters → Permutation."},
      {"q":5,"marks":4,"text":"Fair die rolled. Score=value shown. Find expected value.","answer":"E(X)=(1+2+3+4+5+6)/6=21/6=3.5","hint":"E(X)=Σ[x×P(x)]=1×(1/6)+2×(1/6)+…+6×(1/6)"},
      {"q":6,"marks":5,"text":"Game: win €10(p=0.1), win €5(p=0.2), break even(p=0.3), lose €2(p=0.4). Find E(gain). Worth playing?","answer":"E(X)=1+1+0−0.8=€1.20 per game. Yes, positive expected value → worth playing.","hint":"E(X)=10(0.1)+5(0.2)+0(0.3)+(−2)(0.4)"},
    ]
  },
  { "day":36,"topic":"Statistics","subtopic":"Standard Deviation & Normal Distribution","level":"Higher",
    "block":"Statistics","color":"#6A0572",
    "concept":{"explain":["STANDARD DEVIATION (σ): measures spread around the mean. Steps: (1)Find mean. (2)Subtract mean from each value. (3)Square. (4)Average. (5)Square root.","NORMAL DISTRIBUTION: bell-shaped, symmetric. 68% within ±1σ; 95% within ±2σ; 99.7% within ±3σ."],"analogy":"Standard deviation is measuring consistency. All scores=70% → σ=0 (perfectly consistent). Scores from 10%−100% → large σ (very inconsistent). Tight archery group=small σ.","worked":{"title":"Find σ for 3,5,7,9,11.","steps":["Mean=7","Deviations: −4,−2,0,+2,+4","Squared: 16,4,0,4,16","Variance=40/5=8","σ=√8=2√2≈2.83"]},"mistakes":["Square each deviation SEPARATELY — deviations always sum to 0 by definition","Variance=σ². SD=√(Variance).","Normal: 68% within 1σ means BETWEEN (mean−σ) and (mean+σ)"],"formulae":["σ=√[Σ(x−x̄)²/n]","Normal: 68%:±1σ; 95%:±2σ; 99.7%:±3σ"]},
    "questions":[
      {"q":1,"marks":3,"text":"Find standard deviation of: 3, 4, 5, 6, 7.","answer":"Mean=5. Dev²: 4,1,0,1,4. Variance=2. σ=√2≈1.41","hint":"σ=√[Σ(x−x̄)²/n]. Show each step: deviations, squares, average, square root."},
      {"q":2,"marks":3,"text":"Test marks: mean=70, σ=10, n=200. How many scored between 60 and 80?","answer":"60 to 80 = within 1σ of mean = 68%. 68%×200=136 students","hint":"60=70−10=mean−1σ; 80=70+10=mean+1σ. The 68% rule applies."},
      {"q":3,"marks":4,"text":"Using Q2, how many students scored above 90?","answer":"90=mean+2σ. 5% outside 2σ → 2.5% above 90. 2.5%×200=5 students","hint":"95% within 2σ means 5% outside → 2.5% above and 2.5% below."},
      {"q":4,"marks":4,"text":"Class A: 68,70,71,69,72. Class B: 45,60,70,85,90. Same mean (70). Which has higher σ?","answer":"Class B: spread 45−90 (much wider). Class A: tight cluster 68−72. Class B has higher σ.","hint":"You don't need to calculate — which class has more spread?"},
      {"q":5,"marks":5,"text":"Find standard deviation for: 2, 4, 4, 4, 5, 5, 7, 9. Show all steps.","answer":"Mean=5. Dev²:9,1,1,1,0,0,4,16. Sum=32. Variance=4. σ=2","hint":"Show the table: value, deviation, deviation squared. Average the squared deviations."},
      {"q":6,"marks":5,"text":"Irish men's heights: mean=170cm, σ=8cm, normal distribution. Approx % taller than 185cm?","answer":"185=170+15=mean+1.875σ. Approximately 3% taller than 185cm.","hint":"How many standard deviations is 185 from the mean? Use the 68-95-99.7 rule."},
    ]
  },
  { "day":37,"topic":"Statistics & Probability","subtopic":"Mixed Exam-Style Statistics","level":"Mixed",
    "block":"Statistics","color":"#6A0572",
    "concept":{"explain":["SEC exam stats questions: (a) calculate/draw; (b) use your result; (c) interpret or harder calculation.","INTERPRETATION: write 2+ sentences. State WHAT you found AND WHAT IT MEANS in context. ALWAYS cite your numbers."],"analogy":"Stats exam questions are a story in three chapters: (a) set the scene; (b) develop the plot; (c) the conclusion or twist. Read all three before starting chapter one!","worked":{"title":"SEC stats question strategy","steps":["Read the ENTIRE question — all parts (a)(b)(c) — before writing anything","(a): draw/calculate. Show ALL steps. Label diagrams fully.","(b): look for 'hence' or 'use your answer from (a)'","(c): interpretation — write in FULL SENTENCES citing your numbers","Never leave any part blank — a formula alone earns method marks"]},"mistakes":["'Positive correlation' alone is not enough — explain in context","Histogram: frequency=frequency density×class width","P(A|B): use only the B row/column total, not the grand total"],"formulae":["P(A|B)=P(A∩B)/P(B)","Compare datasets: compare mean (location) AND σ or IQR (spread)","Interpolation: reliable; Extrapolation: unreliable"]},
    "questions":[
      {"q":1,"marks":6,"text":"Heights: 68,72,75,80,63,71,74,76,82,65,70,78,73,90,69,77,75,84,72,88. (a)Mean & median. (b)Range. (c)Modal class (60−70,70−80,80−90). (d)Describe histogram.","answer":"(a)Mean=74.6; Median=75. (b)Range=27. (c)Modal class:70−80. (d)Slightly right-skewed (high value 90).","hint":"Order data for median. For modal class, count values in each group."},
      {"q":2,"marks":6,"text":"Hours x=(2,3,4,5,6,7,8). Scores y=(55,63,70,78,81,88,94). (a)Scatter diagram. (b)Mean point. (c)Predict for 8hrs. (d)Why not predict for 15hrs?","answer":"(a)Positive correlation. (b)(5,75.6). (c)≈90. (d)Extrapolation beyond data range.","hint":"For (b): find x̄ and ȳ. The line MUST pass through (x̄,ȳ)."},
      {"q":3,"marks":6,"text":"Bag: 5R, 7B. Two without replacement. (a)P(1st red). (b)P(both red). (c)P(at least one blue).","answer":"(a)5/12. (b)5/12×4/11=20/132=5/33. (c)1−5/33=28/33","hint":"For (c): use the complement — P(at least one blue)=1−P(both red)."},
      {"q":4,"marks":6,"text":"60 students: 35 study History(H), 30 Science(S), 12 both. (a)Two-way table. (b)P(H∩S). (c)P(H∪S). (d)P(H|S).","answer":"(a)H only=23, both=12, S only=18, neither=7. (b)1/5. (c)53/60. (d)2/5","hint":"For (d): P(H|S)=students in both÷total in S=12/30."},
    ]
  },
  { "day":38,"topic":"Statistics","subtopic":"CBA Investigation Practice","level":"Ordinary",
    "block":"Statistics","color":"#6A0572",
    "concept":{"explain":["CBA 2 at Peppin's Tuition Centre: POSE question→COLLECT data→REPRESENT→ANALYSE→COMMUNICATE. Good question: specific, measurable, has a COMPARISON."],"analogy":"A statistical investigation is science with numbers instead of test tubes. Start with a HYPOTHESIS. Collect data. Analyse. Conclude: does data SUPPORT or REFUTE your hypothesis? Let the DATA speak!","worked":{"title":"Well-posed vs poorly-posed CBA question","steps":["POOR: 'Do students like sport?' (yes/no, not measurable)","BETTER: 'Do 1st year students at Peppin's Tuition Centre spend >2h/week on sport compared to music?'","Why better: specific GROUP, specific VARIABLES, COMPARISON","Analysis: compare mean, median and IQR for both variables","Always state LIMITATIONS: sample size, response bias"]},"mistakes":["Never draw conclusion WITHOUT citing your data values","Small samples (n<30) limit generalisation — mention this!","Response bias: students may answer based on what they THINK they should say"],"formulae":["CBA cycle: Pose→Collect→Represent→Analyse→Communicate","Limitations: sample size, response bias, self-report accuracy"]},
    "questions":[
      {"q":1,"marks":4,"text":"Pose a suitable statistical investigation question for a first-year student. Identify data type and whether to use primary or secondary data.","answer":"E.g. 'Do 1st year students spend more time on social media on weekdays vs weekends?' Primary data: survey. Continuous numerical data.","hint":"Make sure the question is specific, measurable, and has a comparison."},
      {"q":2,"marks":4,"text":"Describe three different sampling methods. Which would you recommend for fairness?","answer":"Random (each person equally likely), Systematic (every kth person), Stratified (proportional from each class). Recommend: stratified — fairest representation.","hint":"Think about how to ensure every group in the year is fairly represented."},
      {"q":3,"marks":5,"text":"Music hours/day: 1,2,3,3,4,4,5,3,4,2. Sport hours: 1,2,2,2,3,3,2,1,3,2. Calculate mean and median for each and compare.","answer":"Music: mean=3.1, median=3. Sport: mean=2.1, median=2. Students spend more time on music (higher mean and median).","hint":"Calculate mean=sum÷count and median=middle value (after ordering) for each."},
      {"q":4,"marks":5,"text":"Using Q3 data, describe how to display the two distributions for comparison.","answer":"Back-to-back stem-and-leaf or side-by-side bar chart. Music values cluster higher (3−4h); Sport lower (2h). Music shows more spread.","hint":"Choose a display that lets you compare both datasets simultaneously."},
      {"q":5,"marks":5,"text":"From Q3, P(>3hrs music) and P(>2hrs sport). Assuming independence, find P(both).","answer":"P(music>3)=4/10=0.4. P(sport>2)=3/10=0.3. P(both)=0.12","hint":"Count values >3 in the music data and >2 in the sport data."},
      {"q":6,"marks":5,"text":"List THREE limitations of the Q3 investigation and suggest improvements.","answer":"1. Small sample (n=10) → increase to 60+. 2. Self-reported data may be inaccurate → use time-tracking app. 3. One-day snapshot → sample over multiple weeks.","hint":"Think about sample size, data accuracy, and time period."},
    ]
  },
  { "day":39,"topic":"Revision","subtopic":"Number & Algebra Rapid-Fire","level":"Mixed",
    "block":"Revision","color":"#C0392B",
    "concept":{"explain":["Rapid-fire revision of Number and Algebra (Days 1−17). Each question tests a different skill — mirroring the opening of the SEC exam.","STRATEGY: the first 4−5 SEC questions are accessible. Use them to build momentum. Show formula first, then substitute — every step earns marks."],"analogy":"Today is a warm-up lap before the race. Revisit every technique at speed — confirm all is working. Like a musician running scales before a concert.","worked":{"title":"Rapid-fire technique","steps":["Write the FORMULA first — earns method marks even if arithmetic slips","Substitute and calculate","Check UNITS and SIGN","Move on — never >4 min on a short question","Return to skipped questions at end"]},"mistakes":["Rushing causes sign errors — always check: positive or negative?","Forgetting to simplify fractions in final answer","Correct formula + wrong values → re-read the question!"],"formulae":["BEMDAS | HCF/LCM | % change | fractions","Solve | Factorise | Quadratic formula | Sequences"]},
    "questions":[
      {"q":1,"marks":2,"text":"Calculate: 3 + 4² × 2 − 1","answer":"4²=16; 16×2=32; 3+32−1=34","hint":"BEMDAS: Exponent first, then multiply, then add/subtract."},
      {"q":2,"marks":2,"text":"Find HCF and LCM of 24 and 36.","answer":"HCF=12; LCM=72","hint":"24=2³×3; 36=2²×3²"},
      {"q":3,"marks":2,"text":"Calculate: 3/8 + 5/6","answer":"LCD=24; 9/24+20/24=29/24=1⁵⁄₂₄","hint":"Find the LCD (24), convert both fractions, then add."},
      {"q":4,"marks":2,"text":"€240 reduced by 15%. Find new price.","answer":"240×0.85=€204","hint":"Multiplier for 15% decrease is (1−0.15)=0.85."},
      {"q":5,"marks":3,"text":"Solve: 5x − 3 = 2x + 12","answer":"3x=15; x=5","hint":"Collect x-terms on one side, numbers on the other."},
      {"q":6,"marks":3,"text":"Expand: (x + 4)(x − 3)","answer":"x²+x−12","hint":"Use FOIL: First, Outer, Inner, Last."},
      {"q":7,"marks":3,"text":"Solve: x² − x − 12 = 0","answer":"(x−4)(x+3)=0; x=4 or x=−3","hint":"Find two numbers: product=−12, sum=−1."},
      {"q":8,"marks":3,"text":"Sequence 3,7,11,15,… Find T₁₀ and Tₙ.","answer":"d=4; Tₙ=4n−1; T₁₀=39","hint":"a=3, d=4. Use Tₙ=a+(n−1)d."},
      {"q":9,"marks":4,"text":"Solve simultaneously: 3x+y=10 and x−2y=−1","answer":"x=2y−1; 6y−3+y=10; y=13/7; x=19/7","hint":"Substitution: rearrange equation 2 to get x=… then substitute."},
      {"q":10,"marks":4,"text":"Write as single fraction: 2/x + 3/(x+1)","answer":"[2(x+1)+3x]/[x(x+1)]=(5x+2)/(x²+x)","hint":"LCD=x(x+1). Convert each fraction, then add numerators."},
    ]
  },
  { "day":40,"topic":"Revision","subtopic":"Geometry & Trig Rapid-Fire","level":"Mixed",
    "block":"Revision","color":"#C0392B",
    "concept":{"explain":["Rapid-fire revision of Geometry and Trigonometry (Days 18−28). These topics account for ~30% of SEC marks — high value!","For proofs: NAME the theorem. For trig: DRAW A DIAGRAM. For coordinate geometry: SHOW the formula before substituting."],"analogy":"Checking all tools in your toolbox before a big job. Each question tests a different tool — confirm every one is ready.","worked":{"title":"Quick formula check","steps":["Distance: |AB|=√[(x₂−x₁)²+(y₂−y₁)²]","Line: y−y₁=m(x−x₁)","Circle: (x−h)²+(y−k)²=r²","SOH CAH TOA | Sine Rule | Cosine Rule — all in Tables booklet","Area: ½bh; ½ab sinC; (θ/360)πr²"]},"mistakes":["Sine vs Cosine Rule: angle BETWEEN two sides → Cosine Rule","Sector perimeter=arc+2 radii (not just arc!)","Perp slope: flip AND change sign. 3/4 → −4/3"],"formulae":["All Geometry & Trig formulae from Days 18−28 apply"]},
    "questions":[
      {"q":1,"marks":2,"text":"Triangle angles: 62°, 74°, x°. Find x.","answer":"x=180−62−74=44°","hint":"Angles in a triangle sum to 180°."},
      {"q":2,"marks":2,"text":"Cylinder half full: r=4cm, h=9cm. Volume of liquid.","answer":"½×π×16×9=72π≈226.2 cm³","hint":"Half the volume of a full cylinder."},
      {"q":3,"marks":3,"text":"Distance between P(2,5) and Q(5,9).","answer":"|PQ|=√[9+16]=5 units","hint":"Apply distance formula."},
      {"q":4,"marks":3,"text":"Slope and midpoint of PQ from Q3.","answer":"m=4/3; midpoint=(3.5,7)","hint":"m=(y₂−y₁)/(x₂−x₁); midpoint=average of coordinates."},
      {"q":5,"marks":3,"text":"Right triangle: legs 8m and 15m. Angle opposite the 15m leg.","answer":"tanθ=15/8 → θ=tan⁻¹(1.875)≈61.9°","hint":"Which trig ratio uses opposite (15m) and adjacent (8m)?"},
      {"q":6,"marks":4,"text":"Sector: r=6cm, θ=72°. Find area.","answer":"(72/360)×π×36=7.2π≈22.6 cm²","hint":"Area=(θ/360)×πr²."},
      {"q":7,"marks":4,"text":"Triangle: two sides 8cm and 6cm, included angle 50°. Find third side.","answer":"c²=64+36−96cos50≈38.3; c≈6.19cm","hint":"SAS → Cosine Rule."},
      {"q":8,"marks":4,"text":"Line through P(2,5) with slope 4/3. Equation as ax+by+c=0.","answer":"y−5=4/3(x−2) → 4x−3y+7=0","hint":"Use y−y₁=m(x−x₁), then rearrange."},
      {"q":9,"marks":4,"text":"Circle (x−3)²+(y+2)²=16. State centre and radius.","answer":"Centre (3,−2), r=4","hint":"Circle (x−h)²+(y−k)²=r². Identify h, k and r."},
      {"q":10,"marks":4,"text":"Area of triangle with vertices (2,2),(5,4),(3,1).","answer":"Area=½|2(4−1)+5(1−2)+3(2−4)|=½×5=2.5 sq units","hint":"Use the coordinate area formula."},
    ]
  },
  { "day":41,"topic":"Revision","subtopic":"Statistics & Probability Rapid-Fire","level":"Mixed",
    "block":"Revision","color":"#C0392B",
    "concept":{"explain":["Rapid-fire revision of Statistics and Probability (Days 29−38). These topics are consistently examined and well-rewarded.","STATS CHECKLIST: Mean (show steps), Median (ORDER data first!), IQR (Q3−Q1), Scatter (show mean point). PROBABILITY CHECKLIST: P(A)=f/total; complement 1−P(A); tree (×along, +across)."],"analogy":"Pre-flight checklist. You are confirming every instrument works before the flight. If any 'fails' (you can't do it), that's what to revise tonight.","worked":{"title":"Quick check — with/without replacement","steps":["Bag: 4R, 6B. Draw 2 WITHOUT replacement.","P(both R)=4/10×3/9=2/15","WITH replacement: P(both R)=4/10×4/10=4/25","Key: WITHOUT replacement — BOTH total (10→9) AND colour count (4→3) decrease"]},"mistakes":["Always ORDER data before finding median or quartiles","Without replacement: update BOTH total AND colour count after each draw","IQR=Q3−Q1 (not range, not Q2−Q1)"],"formulae":["All Stats & Probability formulae from Days 29−38"]},
    "questions":[
      {"q":1,"marks":2,"text":"Mean and median of: 4, 7, 2, 9, 3, 6, 8.","answer":"Mean≈5.57; Ordered: 2,3,4,6,7,8,9. Median=6","hint":"Order data before finding median."},
      {"q":2,"marks":2,"text":"Bag: 3R, 4G, 5Y. P(red)?","answer":"3/12=1/4","hint":"Favourable (3 red) ÷ total (12)."},
      {"q":3,"marks":3,"text":"Fair die: P(score ≥ 4).","answer":"P(4)+P(5)+P(6)=3/6=1/2","hint":"Count how many outcomes satisfy ≥4."},
      {"q":4,"marks":3,"text":"Two from Q2 bag (no replacement). P(both red).","answer":"3/12×2/11=1/22","hint":"After taking one red: 11 left, 2 red."},
      {"q":5,"marks":3,"text":"P(one red, one green) from Q2 bag (no replacement).","answer":"P(RG)+P(GR)=(3/12)(4/11)+(4/12)(3/11)=2/11","hint":"Two orders: RG and GR. Add both probabilities."},
      {"q":6,"marks":4,"text":"Data: 3,1,4,2,3,5,2,1,3,4. Find mode, median and mean.","answer":"Mode=3. Ordered: 1,1,2,2,3,3,3,4,4,5. Median=3. Mean=2.8","hint":"Order data first for median!"},
      {"q":7,"marks":4,"text":"x=(1,2,3,4,5), y=(2,4,5,7,9). Describe correlation and find mean point.","answer":"Strong positive. x̄=3, ȳ=5.4. Mean point (3,5.4)","hint":"The line of best fit must pass through the mean point."},
      {"q":8,"marks":4,"text":"Team wins with P=0.6. Next 2 games: P(win both), P(lose both), P(one each).","answer":"P(WW)=0.36; P(LL)=0.16; P(one each)=0.48","hint":"Independent events: multiply probabilities. One each=P(WL)+P(LW)."},
      {"q":9,"marks":4,"text":"Game: win €2(p=0.3), break even(p=0.5), lose €1(p=0.2). Expected gain.","answer":"E(X)=0.6+0−0.2=€0.40 per game","hint":"E(X)=Σ[x×P(x)]=2(0.3)+0(0.5)+(−1)(0.2)"},
      {"q":10,"marks":4,"text":"Find IQR for: 23,15,29,18,35,20,27,12,31,24. Any outliers? (Use 1.5×IQR rule)","answer":"Q1=18, Q3=27. IQR=9. Fences: 4.5 and 40.5. No outliers.","hint":"Q1=median of lower half; Q3=median of upper half. Outlier if outside Q1−1.5×IQR or Q3+1.5×IQR."},
    ]
  },
  { "day":42,"topic":"Mock Exam","subtopic":"Paper 1: Number, Algebra & Functions","level":"Higher/Ordinary",
    "block":"Mock","color":"#C0392B",
    "concept":{"explain":["TIMED MOCK — Number, Algebra and Functions. Structured exactly like the SEC Junior Cycle Higher Level paper. Time guide: 8−10 minutes per question.","EXAM APPROACH: (1)Read ALL questions first. (2)Start with strongest topic. (3)Show ALL working — formula first. (4)Leave NO part blank. (5)Check answers if time allows."],"analogy":"This mock is your dress rehearsal before the show. Everything is exactly as it will be on the day. No notes, calculator allowed, timed. The feedback from this mock is your most valuable remaining preparation.","worked":{"title":"Multi-part exam question strategy","steps":["Read ALL parts (a)(b)(c) BEFORE writing part (a)","(a): foundational — expand, factorise or calculate. 2−3 steps.","(b): 'hence'=USE part (a) answer. 'Or otherwise'=different method allowed.","(c): hardest — applies skill in context or requires deeper reasoning.","Formula FIRST, then substitute. Show EVERY algebraic step."]},"mistakes":["Ignoring 'hence' — use your previous answer; saves time","Leaving parts blank — always attempt every part for method marks","Not checking quadratic solutions by substituting back in"],"formulae":["All Number & Algebra formulae apply","Quadratic formula in Tables booklet","Tₙ=a+(n−1)d; Sₙ=n/2×[2a+(n−1)d]"]},
    "questions":[
      {"q":1,"marks":10,"text":"(a) Evaluate: 5+3×(8−2)²÷9. (b) Price rises €150→€180. Find % increase. (c) Price falls €120→€108. Find % change.","answer":"(a)17. (b)20% increase. (c)−10% decrease.","hint":"(a)BEMDAS. (b)and(c) % change=(change÷original)×100."},
      {"q":2,"marks":10,"text":"Factorise: (a)6x²−9x. (b)x²−3x−18. (c)2x²+5x+3. Hence solve (b) and (c).","answer":"(a)3x(2x−3). (b)(x−6)(x+3)→x=6 or −3. (c)(2x+3)(x+1)→x=−3/2 or −1","hint":"For 'hence solve': set each factorised expression equal to zero."},
      {"q":3,"marks":10,"text":"Solve: (a)4x−5=2x+7. (b)x/2+(x+1)/3=5. (c)3x+2y=14 and 2x−y=1.","answer":"(a)x=6. (b)x=28/5. (c)x=16/7, y=25/7","hint":"(b)Use LCD=6 to clear fractions. (c)Use elimination or substitution."},
      {"q":4,"marks":10,"text":"f(x)=x²−5x+6. (a)Find f(2). (b)Solve f(x)=0. (c)Find minimum. (d)Sketch graph.","answer":"(a)0. (b)x=2 or 3. (c)Min at x=2.5, f(2.5)=−0.25. (d)Parabola, roots 2 and 3.","hint":"(c)Minimum at x=−b/2a=5/2. (d)Show roots, vertex and y-intercept."},
      {"q":5,"marks":10,"text":"Sequence 5,9,13,17,… (a)Tₙ and T₁₂. (b)S₂₀. (c)Is 201 a term?","answer":"(a)Tₙ=4n+1; T₁₂=49. (b)S₂₀=860. (c)4n+1=201→n=50. Yes, 201 is 50th term.","hint":"(c)Set Tₙ=201 and solve for n. If n is a whole number, it's in the sequence."},
    ]
  },
  { "day":43,"topic":"Mock Exam","subtopic":"Paper 2: Geometry, Trig & Statistics","level":"Higher/Ordinary",
    "block":"Mock","color":"#C0392B",
    "concept":{"explain":["TIMED MOCK — Geometry, Trigonometry and Statistics. Complete under timed conditions. Show ALL working.","GEOMETRY TIPS: write theorem name first; show construction arcs; state units. STATS TIPS: order data before median; label scatter diagram axes; show mean point."],"analogy":"Mock 2 completes the picture. After Paper 1 (algebra) and Paper 2 (geometry+stats), you have experienced the complete exam — the real thing will have no surprises.","worked":{"title":"Stats exam technique — two-way table","steps":["Draw table with ROWS and COLUMNS clearly labelled","Fill given numbers FIRST, then calculate missing","P(A|B): use B column/row TOTAL as denominator","P(A|B)=(A and B)÷(B total) — NOT the grand total"]},"mistakes":["Conditional probability: denominator=GIVEN condition total, not full sample","Cosine Rule: angle A must be OPPOSITE the side a you're finding","Volume in cm³; Surface area in cm²"],"formulae":["All Geometry, Trig & Statistics formulae apply","P(A|B)=P(A∩B)/P(B)"]},
    "questions":[
      {"q":1,"marks":10,"text":"Triangle: ∠A=55°, ∠B=75°, c=12cm. (a)Find ∠C. (b)Find a (Sine Rule). (c)Find area.","answer":"(a)∠C=50°. (b)a≈10.18cm. (c)Area≈46.8 cm²","hint":"(a)Angles sum to 180°. (b)a/sin55=12/sin75. (c)Area=½ac sinB."},
      {"q":2,"marks":10,"text":"P(−1,3), Q(3,5). (a)Slope. (b)|PQ|. (c)Perp bisector equation. (d)Intercepts of perp bisector.","answer":"(a)1/2. (b)2√5. (c)2x+y=6. (d)x-int(3,0); y-int(0,6)","hint":"Perp bisector: through midpoint M=(1,4) with perpendicular slope −2."},
      {"q":3,"marks":10,"text":"Cone: r=6cm, h=8cm. (a)V. (b)Slant h and CSA. (c)Cone on hemisphere (same r). Total V.","answer":"(a)96π≈301.6cm³. (b)l=10cm; CSA=60π. (c)Total=240π≈754cm³","hint":"(c)V_hemisphere=(2/3)πr³. Add cone V + hemisphere V."},
      {"q":4,"marks":10,"text":"Heights: 70,84,72,68,76,65,71,77,74,63. (a)Mean. (b)Median. (c)Q1,Q3,IQR. (d)Outliers?","answer":"(a)72. (b)71.5. (c)Q1=68,Q3=76,IQR=8. (d)No outliers (fences: 56 and 88).","hint":"Order data first: 63,65,68,70,71,72,74,76,77,84."},
      {"q":5,"marks":10,"text":"Bag: 4R, 5B. Two drawn without replacement. (a)P(1st red). (b)P(both red). (c)P(different colours).","answer":"(a)4/9. (b)1/6. (c)5/9","hint":"(c)P(different)=P(RB)+P(BR). Two possible orders."},
    ]
  },
  { "day":44,"topic":"Mock Exam","subtopic":"Full Paper — All Topics","level":"All Topics",
    "block":"Mock","color":"#C0392B",
    "concept":{"explain":["FINAL FULL MOCK — all strands, 90 minutes, no notes, calculator allowed. Mirrors the complete SEC Junior Cycle Mathematics paper.","FINAL MINDSET: You have covered every topic over 44 days. Read carefully. Show working. Trust your preparation.","After completing: mark honestly. Topics where marks were dropped → review that day's concept page tonight."],"analogy":"This is your full concerto rehearsal. A concert pianist plays the complete piece the night before the performance — not to learn it (they already know it), but to build confidence and feel the flow. You have prepared. Trust it.","worked":{"title":"Final exam checklist — before handing in","steps":["Attempted EVERY question and sub-part?","UNITS on every final answer? (cm, cm², cm³, €, °)","FORMULA shown before every calculation?","CHECKED any question I felt unsure about?","All diagrams CLEARLY LABELLED with axes, title and units?"]},"mistakes":["Leaving any part blank — a formula alone earns a method mark","Answer doesn't make sense in context → error (negative area, probability>1)","Spending >3 minutes on one part → move on and return at end"],"formulae":["ALL formulae from all 44 days apply","Tables & Formulae booklet provided in actual SEC exam"]},
    "questions":[
      {"q":1,"marks":8,"text":"(a)4+(6−2)²×3÷8. (b)HCF and LCM of 45 and 60. (c)3/4 of 120 students passed. % failed?","answer":"(a)10. (b)HCF=15,LCM=180. (c)25% failed","hint":"(a)BEMDAS: brackets first. (b)Prime factorise both. (c)1/4 failed."},
      {"q":2,"marks":8,"text":"Solve: (a)2x+5=11. (b)3(x−2)=2x+4. (c)x²−x−6=0.","answer":"(a)x=3. (b)x=10. (c)x=3 or x=−2","hint":"(c)Factorise: find two numbers with product=−6 and sum=−1."},
      {"q":3,"marks":8,"text":"Sequence 5,12,19,26,… (a)Tₙ and T₁₅. (b)Which term=180? (c)S₁₀.","answer":"(a)Tₙ=7n−2; T₁₅=103. (b)26th term. (c)365","hint":"(b)Set 7n−2=180 and solve for n."},
      {"q":4,"marks":8,"text":"Triangle: two angles 58° and y°, exterior angle 130°. (a)Find y. (b)Verify with exterior angle theorem. (c)Triangle type.","answer":"(a)y=72°. (b)58+72=130° ✓. (c)Scalene","hint":"(a)Third interior angle=180−130=50°. So y=180−58−50=72°."},
      {"q":5,"marks":8,"text":"A(1,2), B(7,10). (a)Slope. (b)|AB|. (c)Equation of perp bisector of AB.","answer":"(a)4/3. (b)10. (c)3x+4y=36","hint":"Perp bisector: through midpoint (4,6) with perpendicular slope −3/4."},
      {"q":6,"marks":8,"text":"Cliff: 200m from boat, angle of elevation 35°. (a)Height. (b)Lighthouse 350m from base — angle of elevation?","answer":"(a)200tan35°≈140m. (b)tanα=140/350≈0.4 → α≈21.8°","hint":"(a)tanθ=opposite/adjacent=h/200. (b)Now h is opposite, 350 is adjacent."},
      {"q":7,"marks":8,"text":"(a)Sector area: r=8cm, θ=75°. (b)V of cylinder r=8cm, h=15cm. (c)Total SA of cylinder.","answer":"(a)≈41.9 cm². (b)≈3016 cm³. (c)≈1156 cm²","hint":"(c)Total SA=2πr²+2πrh."},
      {"q":8,"marks":8,"text":"Bag: 5R,8B. Two without replacement. (a)P(1st red). (b)P(both red). (c)P(at least one blue).","answer":"(a)5/13. (b)5/39. (c)34/39","hint":"(c)P(at least one blue)=1−P(both red)=1−5/39."},
      {"q":9,"marks":8,"text":"Ages: 22,30,18,25,21,15,22,27,24,20. Find mean, median, mode, range, Q1, Q3, IQR.","answer":"Mean=22.4; Median=22; Mode=22; Range=15; Q1=20; Q3=25; IQR=5","hint":"Order the data first: 15,18,20,21,22,22,24,25,27,30."},
      {"q":10,"marks":8,"text":"Triangle: AC=7, BC=5, ∠ACB=60°. (i)Find AB. (ii)Area. (iii)Find ∠BAC (Sine Rule).","answer":"(i)AB=√39≈6.24cm. (ii)≈15.16 cm². (iii)≈43.8°","hint":"(i)Cosine Rule. (ii)½ab sinC. (iii)sin(BAC)/5=sin60/6.24."},
    ]
  },
  { "day":45,"topic":"Final Day","subtopic":"Formulae Review & Confidence Builder","level":"All",
    "block":"Revision","color":"#C0392B",
    "concept":{"explain":["FINAL PREPARATION DAY — no new content. Consolidate confidence, review key formulae, complete a targeted practice set.","The 10 questions today are drawn from topics most consistently examined in SEC Junior Cycle papers 2021−2025.","NIGHT BEFORE: review this formulae sheet once. Prepare equipment (calculator, compass, ruler, pencil, eraser). Get a good night's sleep."],"analogy":"Today is the morning of a sports final. The training is done. Stay sharp, keep your eye in, build confidence. No new techniques — reminders of what you know, and belief that you ARE ready.","worked":{"title":"What to bring and remember on exam day","steps":["Equipment: scientific calculator, compass, ruler (30cm), pencil, blue/black pen, eraser","Given in exam: Formulae & Tables booklet — USE IT!","Read each question FULLY before writing. Show EVERY step. Write UNITS.","Method marks available even for arithmetic errors — show your working!","You have done 45 days of focused preparation. You ARE ready."]},"mistakes":["Not using the Tables booklet — formulae for area, volume, trig, sequences all there","Skipping the CHECK step — 10 seconds substituting your answer can save 4 marks","Starting to write before fully reading the question"],"formulae":["BEMDAS • HCF/LCM • % change • Fractions • Ratio","Solve • Factorise • Quadratic formula • Tₙ=a+(n−1)d","Distance • Slope • Line: y−y₁=m(x−x₁) • Circle: (x−h)²+(y−k)²=r²","SOH CAH TOA • Sine Rule • Cosine Rule • Area=½ab sinC","Mean=Σx/n • Median • IQR=Q3−Q1 • P(A)=f/n"]},
    "questions":[
      {"q":1,"marks":3,"text":"Volume of cone: radius 3cm, height 4cm.","answer":"V=⅓π(9)(4)=12π≈37.7 cm³","hint":"V=⅓πr²h. State this formula first!"},
      {"q":2,"marks":3,"text":"Sequence 2,7,12,17,… Find Tₙ and T₈.","answer":"Tₙ=5n−3; T₈=37","hint":"a=2, d=5. Use Tₙ=a+(n−1)d."},
      {"q":3,"marks":3,"text":"Solve: 2x²+3x−2=0","answer":"(2x−1)(x+2)=0; x=1/2 or x=−2","hint":"Find two numbers to factorise. Or use the quadratic formula."},
      {"q":4,"marks":3,"text":"Two fair dice. P(sum=7).","answer":"Pairs: (1,6)(2,5)(3,4)(4,3)(5,2)(6,1)=6/36=1/6","hint":"List all pairs that give a sum of 7. Total outcomes=36."},
      {"q":5,"marks":4,"text":"10m ladder, angle 52° with ground. How high does it reach?","answer":"sin52°=h/10; h≈7.88m","hint":"SOH: sin(angle)=Opposite÷Hypotenuse."},
      {"q":6,"marks":4,"text":"Solve: 3x+4y=25 and x−2y=1","answer":"x=2y+1; 6y+3+4y=25; y=2.2; x=5.4","hint":"Substitution: rearrange x−2y=1 to get x=…"},
      {"q":7,"marks":4,"text":"Find slope and intercepts of 3x+4y=12.","answer":"Slope=−3/4; x-int=(4,0); y-int=(0,3)","hint":"x-intercept: set y=0. y-intercept: set x=0. Slope from y=mx+c form."},
      {"q":8,"marks":5,"text":"Data: 3,1,4,2,3,5,2,1,3,4. Find mean, median, mode and IQR.","answer":"Mean=2.8; Median=3; Mode=3; Q1=2,Q3=4,IQR=2","hint":"Order data first: 1,1,2,2,3,3,3,4,4,5."},
      {"q":9,"marks":5,"text":"Bag: 6R,9B. 3 drawn without replacement. P(exactly 2R, 1B).","answer":"⁶C₂×⁹C₁/¹⁵C₃=15×9/455=27/91","hint":"Use combinations: C(6,2)×C(9,1)÷C(15,3)."},
      {"q":10,"marks":5,"text":"Triangle sides 9cm, 8cm, 10cm. Find the largest angle.","answer":"cosA=(64+81−100)/(2×8×9)=45/144≈0.3125; A≈71.8°","hint":"Largest angle is opposite longest side (10cm). Use Cosine Rule."},
    ]
  },
]

BLOCKS = {
  "Number": {"color": "#1B3A6B", "icon": "🔢"},
  "Algebra": {"color": "#2E7D32", "icon": "✖️"},
  "Geometry": {"color": "#B8860B", "icon": "📐"},
  "Statistics": {"color": "#6A0572", "icon": "📊"},
  "Revision": {"color": "#C0392B", "icon": "📝"},
  "Mock": {"color": "#C0392B", "icon": "📋"},
}

# ─── HTML GENERATORS ───────────────────────────────────────────────────────────

def html_head(title, extra_css=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Merriweather:wght@700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
{extra_css}
</head>"""

def generate_css():
    return """:root {
  --navy: #1B3A6B;
  --green: #2E7D32;
  --gold: #C8960C;
  --red: #C0392B;
  --purple: #6A0572;
  --bg: #F7F8FC;
  --card: #FFFFFF;
  --text: #1A1A2E;
  --muted: #6B7280;
  --border: #E5E7EB;
  --radius: 14px;
  --shadow: 0 2px 12px rgba(0,0,0,0.08);
  --shadow-lg: 0 8px 32px rgba(0,0,0,0.12);
}

*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Nunito',sans-serif;background:var(--bg);color:var(--text);min-height:100vh;font-size:16px;line-height:1.6;}
a{color:inherit;text-decoration:none;}

/* ── Navbar ── */
.navbar{position:sticky;top:0;z-index:100;background:#fff;border-bottom:3px solid var(--navy);display:flex;align-items:center;gap:1rem;padding:.75rem 1.5rem;box-shadow:0 2px 8px rgba(0,0,0,.06);}
.nav-brand{display:flex;align-items:center;gap:.6rem;margin-right:auto;}
.nav-logo{font-size:1.6rem;}
.nav-title{font-weight:900;font-size:1.05rem;color:var(--navy);line-height:1.1;}
.nav-sub{font-size:.7rem;color:var(--muted);}
.nav-links{display:flex;gap:.3rem;flex-wrap:wrap;}
.nav-link{padding:.4rem .8rem;border-radius:8px;font-weight:700;font-size:.85rem;transition:all .2s;color:var(--muted);}
.nav-link:hover,.nav-link.active{background:var(--navy);color:#fff;}
.nav-toggle{display:none;background:none;border:2px solid var(--navy);border-radius:8px;padding:.3rem .6rem;cursor:pointer;font-size:1.1rem;color:var(--navy);}
@media(max-width:680px){
  .nav-links{display:none;position:absolute;top:100%;left:0;right:0;background:#fff;flex-direction:column;padding:1rem;border-bottom:2px solid var(--border);box-shadow:0 8px 20px rgba(0,0,0,.1);}
  .nav-links.open{display:flex;}
  .nav-toggle{display:block;}
}

/* ── Layout ── */
.container{max-width:1100px;margin:0 auto;padding:1.5rem 1rem;}
.page-hero{background:linear-gradient(135deg,var(--navy) 0%,#2d5496 100%);color:#fff;padding:2.5rem 1.5rem;text-align:center;}
.page-hero h1{font-family:'Merriweather',serif;font-size:clamp(1.5rem,4vw,2.4rem);margin-bottom:.5rem;}
.page-hero p{font-size:1rem;opacity:.85;max-width:600px;margin:0 auto;}
.badge{display:inline-block;padding:.25rem .7rem;border-radius:20px;font-size:.75rem;font-weight:700;letter-spacing:.03em;}

/* ── Cards ── */
.card{background:var(--card);border-radius:var(--radius);box-shadow:var(--shadow);overflow:hidden;transition:transform .2s,box-shadow .2s;}
.card:hover{transform:translateY(-3px);box-shadow:var(--shadow-lg);}
.card-header{padding:1rem 1.25rem;display:flex;align-items:center;gap:.75rem;}
.card-body{padding:1rem 1.25rem;}

/* ── Grid ── */
.grid-2{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:1.25rem;}
.grid-3{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:1rem;}

/* ── Day card ── */
.day-card{border-left:5px solid var(--navy);cursor:pointer;}
.day-num{font-size:.7rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase;opacity:.8;}
.day-topic{font-weight:800;font-size:1rem;margin:.1rem 0;}
.day-sub{font-size:.82rem;color:var(--muted);}
.day-meta{display:flex;gap:.5rem;align-items:center;margin-top:.6rem;flex-wrap:wrap;}
.level-badge{padding:.2rem .55rem;border-radius:12px;font-size:.7rem;font-weight:700;color:#fff;}
.completed-mark{margin-left:auto;font-size:1.1rem;}

/* ── Concept page ── */
.concept-section{margin-bottom:1.25rem;}
.section-label{font-size:.7rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase;margin-bottom:.5rem;display:flex;align-items:center;gap:.4rem;}
.explain-box{background:#EAF4FB;border-left:5px solid #1565C0;border-radius:8px;padding:1rem 1.25rem;}
.explain-box p{margin:.4rem 0;font-size:.95rem;}
.analogy-box{background:#FFF8E1;border-left:5px solid var(--gold);border-radius:8px;padding:1rem 1.25rem;}
.mistake-box{background:#FBE9E7;border-left:5px solid #BF360C;border-radius:8px;padding:1rem 1.25rem;}
.mistake-box li{margin:.3rem 0;font-size:.95rem;}
.formula-box{background:#EEF2FF;border:2px solid var(--navy);border-radius:8px;padding:1rem 1.25rem;}
.formula-box code{display:block;font-family:'Courier New',monospace;font-size:.95rem;font-weight:700;margin:.25rem 0;color:var(--navy);}
.worked-box{background:#E8F5E9;border-left:5px solid var(--green);border-radius:8px;padding:1rem 1.25rem;}
.step-list{list-style:none;counter-reset:steps;}
.step-list li{counter-increment:steps;display:flex;gap:.75rem;margin:.5rem 0;align-items:flex-start;}
.step-list li::before{content:counter(steps);background:var(--green);color:#fff;border-radius:50%;width:24px;height:24px;display:flex;align-items:center;justify-content:center;font-size:.75rem;font-weight:800;flex-shrink:0;margin-top:.1rem;}

/* ── Question card ── */
.question-card{background:var(--card);border-radius:12px;box-shadow:var(--shadow);margin-bottom:1rem;overflow:hidden;}
.q-header{display:flex;align-items:center;gap:.75rem;padding:.8rem 1.1rem;background:var(--navy);color:#fff;}
.q-num{background:rgba(255,255,255,.2);border-radius:8px;padding:.2rem .55rem;font-weight:800;font-size:.85rem;}
.q-marks{margin-left:auto;font-size:.75rem;opacity:.75;}
.q-text{padding:.9rem 1.1rem;font-size:.97rem;line-height:1.7;}
.q-hint{background:#FFFDE7;border-top:1px dashed #FFD54F;padding:.6rem 1.1rem;font-size:.83rem;color:#5D4037;display:none;}
.q-answer{background:#F1F8E9;border-top:1px solid #C8E6C9;padding:.8rem 1.1rem;font-size:.88rem;display:none;}
.q-answer strong{color:var(--green);}
.q-actions{padding:.6rem 1.1rem;display:flex;gap:.5rem;flex-wrap:wrap;border-top:1px solid var(--border);}
.btn{display:inline-flex;align-items:center;gap:.35rem;padding:.45rem .9rem;border-radius:8px;font-size:.82rem;font-weight:700;cursor:pointer;border:none;transition:all .2s;font-family:'Nunito',sans-serif;}
.btn-hint{background:#FFF9C4;color:#5D4037;border:1px solid #FFD54F;}
.btn-hint:hover{background:#FFE082;}
.btn-answer{background:#E8F5E9;color:#1B5E20;border:1px solid #A5D6A7;}
.btn-answer:hover{background:#C8E6C9;}
.btn-primary{background:var(--navy);color:#fff;}
.btn-primary:hover{background:#2d5496;}
.btn-green{background:var(--green);color:#fff;}
.btn-green:hover{background:#1B5E20;}
.btn-red{background:var(--red);color:#fff;}
.btn-red:hover{background:#922b21;}
.btn-gold{background:var(--gold);color:#fff;}
.btn-gold:hover{background:#a57c0a;}
.btn-sm{padding:.3rem .65rem;font-size:.75rem;}
.btn-lg{padding:.7rem 1.4rem;font-size:1rem;}
.btn-block{width:100%;justify-content:center;}

/* ── Progress bar ── */
.progress-bar{background:var(--border);border-radius:20px;height:10px;overflow:hidden;margin:.35rem 0;}
.progress-fill{height:100%;border-radius:20px;transition:width .6s ease;}
.progress-label{display:flex;justify-content:space-between;font-size:.75rem;color:var(--muted);}

/* ── Quiz ── */
.quiz-option{display:block;padding:.8rem 1.1rem;border:2px solid var(--border);border-radius:10px;margin:.5rem 0;cursor:pointer;font-weight:600;transition:all .18s;background:#fff;}
.quiz-option:hover{border-color:var(--navy);background:#F0F4FF;}
.quiz-option.correct{border-color:var(--green);background:#E8F5E9;color:var(--green);}
.quiz-option.incorrect{border-color:var(--red);background:#FFEBEE;color:var(--red);}
.quiz-score{text-align:center;padding:2rem;font-size:3rem;font-weight:900;}

/* ── Stats strip ── */
.stats-strip{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:.75rem;margin:1.25rem 0;}
.stat-box{background:var(--card);border-radius:12px;padding:1rem;text-align:center;box-shadow:var(--shadow);}
.stat-num{font-size:1.8rem;font-weight:900;line-height:1;}
.stat-label{font-size:.72rem;color:var(--muted);margin-top:.25rem;}

/* ── Tabs ── */
.tab-bar{display:flex;gap:.3rem;margin:1rem 0;border-bottom:2px solid var(--border);overflow-x:auto;padding-bottom:-2px;}
.tab{padding:.55rem 1rem;font-weight:700;font-size:.88rem;border-radius:8px 8px 0 0;cursor:pointer;color:var(--muted);background:none;border:none;border-bottom:3px solid transparent;transition:all .2s;white-space:nowrap;font-family:'Nunito',sans-serif;}
.tab.active{color:var(--navy);border-bottom-color:var(--navy);background:#f0f4ff;}
.tab-content{display:none;}
.tab-content.active{display:block;}

/* ── Misc ── */
.mt1{margin-top:.5rem;} .mt2{margin-top:1rem;} .mt3{margin-top:1.5rem;} .mt4{margin-top:2rem;}
.mb1{margin-bottom:.5rem;} .mb2{margin-bottom:1rem;}
.flex{display:flex;} .flex-center{align-items:center;} .gap{gap:.75rem;}
.text-center{text-align:center;}
.muted{color:var(--muted);}
.emoji-big{font-size:2.5rem;}
.tip-box{background:#FFF3E0;border-left:4px solid var(--gold);border-radius:8px;padding:.9rem 1.1rem;font-size:.9rem;color:#4E342E;}
.inline-correct{color:var(--green);font-weight:800;}
.back-link{display:inline-flex;align-items:center;gap:.4rem;color:var(--navy);font-weight:700;font-size:.88rem;margin-bottom:1rem;padding:.4rem .8rem;border-radius:8px;border:2px solid var(--border);}
.back-link:hover{background:var(--navy);color:#fff;border-color:var(--navy);}
footer{background:var(--navy);color:rgba(255,255,255,.7);text-align:center;padding:1.5rem;font-size:.82rem;margin-top:3rem;}
footer strong{color:#fff;}
"""


def level_color(level):
    if "Higher" in level: return "#C0392B"
    if "Ordinary" in level: return "#1B3A6B"
    if "Foundation" in level: return "#B8860B"
    if "Mixed" in level or "All" in level: return "#6A0572"
    return "#555"


def generate_plan():
    rows = ""
    prev_block = None
    for d in DAYS:
        if d["block"] != prev_block:
            info = BLOCKS.get(d["block"], {"color":"#555","icon":"📚"})
            rows += f"""<tr><td colspan="5" style="background:{info['color']};color:#fff;font-weight:800;padding:.6rem 1rem;font-size:.9rem;">{info['icon']} {d['block']} Block · Days {d['day']}–</td></tr>\n"""
            prev_block = d["block"]
        lc = level_color(d["level"])
        qs = len(d["questions"])
        rows += f"""<tr>
  <td><a href="day{d['day']}.html" style="font-weight:800;color:var(--navy);">Day {d['day']}</a></td>
  <td><strong>{d['topic']}</strong></td>
  <td>{d['subtopic']}</td>
  <td><span class="level-badge" style="background:{lc}">{d['level']}</span></td>
  <td style="text-align:center">{qs}</td>
</tr>\n"""

    body = f"""
{nav_bar("plan")}
<div class="page-hero">
  <h1>📅 45-Day Study Plan</h1>
  <p>Every day = Concept Explanation + Practice Questions + Worked Answers</p>
</div>
<div class="container">
<div style="overflow-x:auto;margin-top:1.5rem;">
<table style="width:100%;border-collapse:collapse;background:#fff;border-radius:var(--radius);overflow:hidden;box-shadow:var(--shadow);">
  <thead>
    <tr style="background:var(--navy);color:#fff;">
      <th style="padding:.7rem 1rem;text-align:left;font-size:.85rem;">Day</th>
      <th style="padding:.7rem 1rem;text-align:left;font-size:.85rem;">Topic</th>
      <th style="padding:.7rem 1rem;text-align:left;font-size:.85rem;">Subtopic</th>
      <th style="padding:.7rem 1rem;text-align:left;font-size:.85rem;">Level</th>
      <th style="padding:.7rem 1rem;text-align:center;font-size:.85rem;">Questions</th>
    </tr>
  </thead>
  <tbody style="font-size:.9rem;">
{rows}
  </tbody>
</table>
</div>
</div>
<footer>
  <strong>Peppin's Tuition Centre, Cork</strong> · Junior Cycle Mathematics · 45-Day Tuition Programme
</footer>
"""
    return html_head("45-Day Plan · Peppin's Maths") + "<body>" + body + "</body></html>"


def generate_quiz():
    import random as rng
    # Build 20 questions from across all days
    all_qs = []
    for d in DAYS:
        for q in d["questions"]:
            all_qs.append({
                "day": d["day"], "topic": d["topic"], "color": d["color"],
                "text": q["text"], "answer": q["answer"], "hint": q["hint"],
                "marks": q["marks"]
            })

    # Select a spread of 20
    selected = []
    # Take 1 from each block section roughly
    blocks_order = ["Number","Algebra","Geometry","Statistics","Revision","Mock"]
    qs_by_block = {}
    for d in DAYS:
        qs_by_block.setdefault(d["block"],[]).extend(
            [{"day":d["day"],"topic":d["topic"],"color":d["color"],"text":q["text"],
              "answer":q["answer"],"hint":q["hint"],"marks":q["marks"]} for q in d["questions"]]
        )
    # For the quiz, we'll use JS to randomly pick questions from embedded data
    all_q_json = json.dumps([
        {"day":d["day"],"topic":d["topic"],"color":d["color"],"text":q["text"],
         "answer":q["answer"],"hint":q["hint"],"marks":q["marks"]}
        for d in DAYS for q in d["questions"]
    ])

    body = f"""
{nav_bar("quiz")}
<div class="page-hero">
  <h1>⚡ Quick Quiz</h1>
  <p>Test yourself across the full Junior Cycle syllabus · Questions are randomly selected</p>
</div>

<div class="container" style="max-width:750px;">
  <div id="quiz-setup" class="card mt3" style="padding:1.5rem;text-align:center;">
    <div style="font-size:3rem;margin-bottom:1rem">🎯</div>
    <h2 style="margin-bottom:.5rem">Choose Your Quiz</h2>
    <p class="muted mb2">Select a topic and number of questions</p>
    <div style="display:flex;flex-direction:column;gap:.75rem;max-width:380px;margin:0 auto;">
      <select id="topic-select" class="quiz-select" style="padding:.7rem 1rem;border-radius:10px;border:2px solid var(--border);font-family:'Nunito',sans-serif;font-size:.95rem;font-weight:600;">
        <option value="all">🌐 All Topics (Random)</option>
        <option value="Number">🔢 Number</option>
        <option value="Algebra">✖️ Algebra</option>
        <option value="Geometry">📐 Geometry</option>
        <option value="Statistics">📊 Statistics & Probability</option>
        <option value="Revision">📝 Revision & Mock</option>
      </select>
      <select id="count-select" style="padding:.7rem 1rem;border-radius:10px;border:2px solid var(--border);font-family:'Nunito',sans-serif;font-size:.95rem;font-weight:600;">
        <option value="5">5 Questions (Quick)</option>
        <option value="10" selected>10 Questions (Standard)</option>
        <option value="15">15 Questions (Extended)</option>
        <option value="20">20 Questions (Full)</option>
      </select>
      <button class="btn btn-primary btn-lg btn-block" onclick="startQuiz()">🚀 Start Quiz</button>
    </div>
  </div>

  <div id="quiz-area" style="display:none">
    <div style="display:flex;align-items:center;gap:1rem;margin:1rem 0;">
      <div id="q-progress-label" style="font-weight:800;color:var(--navy);min-width:80px;"></div>
      <div class="progress-bar" style="flex:1"><div class="progress-fill" id="q-progress-fill" style="background:var(--navy);width:0%"></div></div>
      <div id="q-score-label" style="font-weight:800;color:var(--green);min-width:60px;text-align:right;"></div>
    </div>

    <div id="question-card" class="question-card">
      <div class="q-header" id="q-topic-bar">
        <span class="q-num" id="q-num-label"></span>
        <span id="q-topic-label" style="font-size:.8rem;opacity:.8;margin-left:auto;"></span>
      </div>
      <div class="q-text" id="q-text" style="font-size:1.05rem;padding:1.25rem;"></div>
      <div style="padding:.75rem 1.1rem;">
        <div id="q-hint-box" class="q-hint" style="display:none;margin-bottom:.5rem;"></div>
        <button class="btn btn-hint btn-sm" onclick="showHint()">💡 Show Hint</button>
      </div>
      <div style="padding:1rem 1.1rem;border-top:1px solid var(--border);">
        <div style="font-size:.82rem;color:var(--muted);margin-bottom:.5rem;font-weight:700;">How did you do on this question?</div>
        <div style="display:flex;gap:.5rem;flex-wrap:wrap;">
          <button class="btn btn-green" onclick="markAnswer(true)">✅ Got it right!</button>
          <button class="btn btn-red" onclick="markAnswer(false)">❌ Got it wrong</button>
        </div>
        <div id="q-answer-reveal" style="display:none;margin-top:.75rem;background:#F1F8E9;border-radius:8px;padding:.8rem;font-size:.9rem;">
          <strong style="color:var(--green)">✅ Answer:</strong> <span id="q-answer-text"></span>
        </div>
      </div>
    </div>
  </div>

  <div id="quiz-result" style="display:none;text-align:center;padding:2rem 1rem;">
    <div id="result-emoji" class="quiz-score"></div>
    <h2 id="result-title" style="font-family:'Merriweather',serif;margin-bottom:.5rem;"></h2>
    <p id="result-sub" class="muted mb2"></p>
    <div id="result-bar" style="max-width:300px;margin:1rem auto;"></div>
    <div style="display:flex;gap:.75rem;justify-content:center;flex-wrap:wrap;margin-top:1.5rem;">
      <button class="btn btn-primary btn-lg" onclick="resetQuiz()">🔄 Try Again</button>
      <a href="plan.html" class="btn btn-gold btn-lg">📅 Study Plan</a>
    </div>
    <div id="result-review" style="margin-top:2rem;text-align:left;"></div>
  </div>
</div>

<footer>
  <strong>Peppin's Tuition Centre, Cork</strong> · Junior Cycle Mathematics Quiz
</footer>

<script>
const ALL_QUESTIONS = {all_q_json};
let questions=[], current=0, score=0, wrong=[];

function startQuiz(){{
  const topic=document.getElementById('topic-select').value;
  const count=parseInt(document.getElementById('count-select').value);
  let pool=topic==='all'?[...ALL_QUESTIONS]:ALL_QUESTIONS.filter(q=>{{
    return ALL_QUESTIONS.indexOf(q)>=0; // filter by block handled below
  }});
  // filter by block
  if(topic!=='all'){{
    const daysByBlock={{}};
    {json.dumps({d['day']:d['block'] for d in DAYS})};
    const dm={json.dumps({d['day']:d['block'] for d in DAYS})};
    pool=ALL_QUESTIONS.filter(q=>dm[q.day]===topic);
  }}
  // shuffle
  pool=[...pool].sort(()=>Math.random()-.5);
  questions=pool.slice(0,count);
  current=0; score=0; wrong=[];
  document.getElementById('quiz-setup').style.display='none';
  document.getElementById('quiz-area').style.display='block';
  document.getElementById('quiz-result').style.display='none';
  showQuestion();
}}

function showQuestion(){{
  if(current>=questions.length){{showResult();return;}}
  const q=questions[current];
  document.getElementById('q-num-label').textContent='Q'+(current+1);
  document.getElementById('q-topic-label').textContent='Day '+q.day+' · '+q.topic;
  document.getElementById('q-topic-bar').style.background=q.color||'var(--navy)';
  document.getElementById('q-text').textContent=q.text;
  document.getElementById('q-hint-box').textContent='💡 '+q.hint;
  document.getElementById('q-hint-box').style.display='none';
  document.getElementById('q-answer-reveal').style.display='none';
  document.getElementById('q-answer-text').textContent=q.answer;
  document.getElementById('q-progress-label').textContent=(current+1)+' / '+questions.length;
  document.getElementById('q-score-label').textContent='Score: '+score;
  const pct=Math.round(current/questions.length*100);
  document.getElementById('q-progress-fill').style.width=pct+'%';
}}

function showHint(){{document.getElementById('q-hint-box').style.display='block';}}

function markAnswer(correct){{
  document.getElementById('q-answer-reveal').style.display='block';
  if(correct) score++;
  else wrong.push(questions[current]);
  setTimeout(()=>{{current++;showQuestion();}},1800);
}}

function showResult(){{
  document.getElementById('quiz-area').style.display='none';
  document.getElementById('quiz-result').style.display='block';
  const total=questions.length;
  const pct=Math.round(score/total*100);
  let emoji,title,sub;
  if(pct>=90){{emoji='🌟';title='Outstanding!';sub='Excellent work — you know this material really well.';}}
  else if(pct>=75){{emoji='💪';title='Great Work!';sub='Strong performance. Review the questions you missed.';}}
  else if(pct>=55){{emoji='📚';title='Good Effort!';sub='Keep practising — revisit the concept pages for the topics you missed.';}}
  else{{emoji='🔄';title='Keep Going!';sub='Go back to the concept pages for these topics and try again.';}}
  document.getElementById('result-emoji').textContent=emoji;
  document.getElementById('result-title').textContent=title+' '+score+'/'+total+' ('+pct+'%)';
  document.getElementById('result-sub').textContent=sub;
  if(wrong.length>0){{
    let html='<h3 style="margin-bottom:.75rem;color:var(--red)">❌ Review These Questions:</h3>';
    wrong.forEach(q=>{{
      html+=`<div class="question-card" style="margin-bottom:.75rem">
        <div class="q-header" style="background:${{q.color||'var(--navy)'}}">
          <span style="font-size:.78rem;opacity:.8">Day ${{q.day}} · ${{q.topic}}</span>
        </div>
        <div class="q-text">${{q.text}}</div>
        <div style="padding:.8rem 1.1rem;background:#F1F8E9;font-size:.88rem">
          <strong style="color:var(--green)">✅ Answer:</strong> ${{q.answer}}
        </div>
      </div>`;
    }});
    document.getElementById('result-review').innerHTML=html;
  }}
}}

function resetQuiz(){{
  document.getElementById('quiz-setup').style.display='block';
  document.getElementById('quiz-area').style.display='none';
  document.getElementById('quiz-result').style.display='none';
}}
</script>
"""
    return html_head("Quick Quiz · Peppin's Maths") + "<body>" + body + "</body></html>"


def generate_readme():
    return """# Peppin's Tuition Centre, Cork — Junior Cycle Mathematics Study App

## 🍀 Live Study App

**➡️ Open the app:** [https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/](https://your-username.github.io/your-repo-name/)

A complete, mobile-friendly Junior Cycle Maths study app for First Year students at Peppin's Tuition Centre, Cork. Covers all 45 days of the tuition programme.

## Features

- 📖 **Concept pages** with tutor explanations, analogies, worked examples and common mistakes
- ✏️ **Practice questions** with hints and worked answers (6–10 per day)
- ⚡ **Quiz mode** — random questions across all topics with instant feedback
- 📈 **Progress tracker** — mark days complete, stored in your browser
- 📐 **Fully responsive** — works on mobile, tablet and desktop
- 🚫 **No server needed** — pure HTML/CSS/JS, works offline after first load

## Topics Covered (45 Days)

| Block | Days | Topics |
|-------|------|--------|
| Number | 1–7 | Place Value, BEMDAS, Factors, Integers, Fractions, Decimals, %, Sets, Ratio, Tax |
| Algebra | 8–17 | Expressions, Expanding, Factorising, Equations, Simultaneous, Quadratics, Functions |
| Geometry | 18–28 | Angles, Theorems, Constructions, Area, Volume, Coordinate Geometry, Trigonometry |
| Statistics | 29–38 | Data, Mean/Median, Charts, Scatter, Probability, Counting, Normal Distribution, CBA |
| Revision | 39–45 | Rapid-fire reviews + 3 full mock exam papers |

## Running Locally

```bash
python3 generate.py
cd docs
python3 -m http.server 8080
# Open http://localhost:8080
```

## Publishing to GitHub Pages

1. Push this repository to GitHub
2. Go to **Settings → Pages**
3. Under **Source**, select `Deploy from a branch`
4. Choose **Branch: main** and **Folder: /docs**
5. Click **Save**
6. Your app will be live at `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/` within a few minutes

## Regenerating the App

If you modify `generate.py`, regenerate the site:

```bash
python3 generate.py
```

All output goes into the `docs/` folder, ready to commit and push.

## Aligned To

- NCCA Junior Cycle Mathematics Specification 2018
- SEC Junior Cycle Exam Papers 2021–2025
- Peppin's Tuition Centre, Cork teaching sequence

---
*Built for Peppin's Tuition Centre Junior Cycle Maths Tuition Programme*
"""


def generate_404():
    return """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Page Not Found</title>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css"></head>
<body style="display:flex;align-items:center;justify-content:center;min-height:100vh;text-align:center;padding:2rem;">
  <div>
    <div style="font-size:4rem">📐</div>
    <h1 style="font-size:2rem;color:var(--navy);margin:.5rem 0">Page Not Found</h1>
    <p style="color:var(--muted);margin-bottom:1.5rem">Looks like this equation has no solution!</p>
    <a href="index.html" class="btn btn-primary btn-lg">🏠 Go Home</a>
  </div>
</body></html>"""


# ─── INJECT TIPS ─────────────────────────────────────────────────────────────
_TIPS = {1: 'BEMDAS appears in ~80% of SEC papers in Q1. Always show each step on a separate line — each step earns marks even if you make an arithmetic error later.', 2: 'HCF/LCM: the most common error is confusing HCF (lowest powers) with LCM (highest powers). Prime factorisation always works and is worth showing in full.', 3: 'Directed numbers are tested inside almost every algebra question. The most penalised error: not using brackets around negative substitutions, e.g. x=−3 must become (−3)²=9.', 4: 'Fractions appear in Q1 and embedded in algebra. The SEC awards marks for showing the LCD step even if the final answer is wrong — never skip it.', 5: '% change is in every paper. Always divide by the ORIGINAL value. Two successive % changes must be applied separately — never add the percentages together.', 6: "Venn diagrams appear in Q6 most years. Always fill the INTERSECTION (both) first, then find 'only A' and 'only B' by subtracting. Formula |A∪B|=|A|+|B|−|A∩B| is in the Tables booklet.", 7: 'Ratio and tax questions: always calculate each income tax band separately; subtract credits AFTER calculating gross tax. The multiplier method (×1.12 for VAT) is fastest.', 8: 'Algebra substitution: put negative values in BRACKETS every time. The examiner awards a method mark for your substitution step, even before any arithmetic is done.', 9: 'Expanding double brackets is tested in almost every Q2. The DoTS pattern (a+b)(a−b)=a²−b² saves time and is heavily used in later algebraic fractions questions.', 10: 'Factorising: SEC examiners award marks for each correct factor. Always CHECK by expanding — takes 10 seconds and can confirm or save 4 marks.', 11: 'Linear equations: the SEC always awards method marks for expanding brackets, collecting terms, and the final answer separately. Never skip showing the CHECK substitution.', 12: 'Simultaneous equations appear every year, often in word-problem context. The elimination method is most reliable. ALWAYS verify both values in BOTH original equations.', 13: 'Quadratic equations appear in at least 2 questions yearly. The quadratic formula is in the Tables & Formulae booklet — you must know when to use it. Check solutions by substituting back.', 14: "Sequence questions: common SEC pattern is (a) find Tₙ; (b) find a specific term; (c) 'is x a term?' Set Tₙ=value, solve for n. If n is a whole number, yes — it is in the sequence.", 15: 'Functions: always make a TABLE of at least 5 values before drawing — never sketch freehand. Roots and turning point are common part (c) questions worth significant marks.', 16: 'Algebraic fractions appear in Higher Level. Key: factorise BOTH numerator and denominator before cancelling. Only cancel FACTORS (things that multiply), never TERMS (things that add).', 17: "Mixed algebra mirrors the SEC format. Read all parts (a)(b)(c) before writing anything. 'Hence' means use your previous answer — the link is always deliberate and saves calculation.", 18: "Angle theorems: always NAME the theorem before applying it. 'By the Exterior Angle Theorem…' — naming earns marks in proofs even if a calculation step has errors.", 19: 'Circle Theorem 6 (angle at centre = 2×angle at circumference) is the most tested. Corollary (angle in semicircle = 90°) appears in nearly every SEC paper — know it cold.', 20: 'Constructions: never erase your compass arcs — they show the examiner you used the correct geometric method and earn construction marks even if the final shape is imprecise.', 21: 'Area and sectors: sector perimeter = arc + TWO radii (students often forget the two straight sides). All formulae are in the Tables booklet — use it for every calculation.', 22: 'Volume: composite solid questions are common. Calculate each part separately and ADD. Cone slant height l=√(r²+h²) must be calculated using Pythagoras — it is not given directly.', 23: 'Coordinate geometry: perpendicular slope (−1/m) is frequently needed. Remember: perpendicular means FLIP the fraction AND CHANGE the sign. m=3/4 → m⊥=−4/3.', 24: "Circle equations: practice 'state centre and radius', 'find where circle meets axes', and 'is point inside/outside?' These three are the most common part-types in SEC questions.", 25: 'SOH CAH TOA appears in every paper. Draw a labelled diagram FIRST. Calculator must be in DEGREE mode. Angle of elevation/depression is always measured from the HORIZONTAL.', 26: 'Sine/Cosine Rule decision: angle BETWEEN two sides and you know them → Cosine Rule. Know one angle and opposite side + another side → Sine Rule. Area=½ab sinC is in the booklet.', 27: 'Multi-step geometry: always show sub-answers clearly labelled. If an early step is wrong, consequential marks reward correct use of your wrong value in all subsequent steps.', 28: 'Coordinate geometry questions follow a consistent SEC pattern: (a) slope/distance/midpoint; (b) equation of line or circle; (c) intersection or inside/outside. Practice this 3-part structure.', 29: 'Statistics questions: drawing a neat, labelled frequency table — even if not explicitly asked — demonstrates organised thinking and earns presentation marks.', 30: 'Mean, median and IQR: the most common error is finding median WITHOUT ordering data first. Write the ordered list as your very first step — every time.', 31: 'Histograms: if class widths are EQUAL, y-axis can show frequency. If widths DIFFER, y-axis MUST show frequency density=freq÷class width. Check widths before drawing.', 32: 'Scatter diagrams: the line of best fit MUST pass through the mean point (x̄,ȳ). Mark the mean point as a cross on the diagram BEFORE drawing the line. Examiners look for this explicitly.', 33: 'Basic probability: P(A or B)=P(A)+P(B) ONLY for mutually exclusive events. If events can overlap (e.g. even AND prime on a die), always subtract P(A∩B) to avoid double-counting.', 34: 'Tree diagrams: without replacement — BOTH the total and the selected colour count must decrease after each draw. Always verify all terminal branches sum to exactly 1.', 35: "Counting principles: ask 'does order matter?' Roles (president, secretary) → order matters → Permutation nPr. Committees/groups → order doesn't matter → Combination nCr.", 36: 'Standard deviation and normal distribution: the 68-95-99.7 rule is the most tested. 68% within ±1σ; 95% within ±2σ. Show the full σ calculation step by step — each step earns marks.', 37: "Statistics exam part (c) is usually interpretation. Write at least 2 sentences, name BOTH variables, and cite the specific numbers you calculated. 'Positive correlation' alone is not enough.", 38: "CBA 2 at Peppin's Tuition Centre is your statistical investigation. The most common weakness: vague conclusions. Always write: 'My data shows X because mean hours sport (Y) > mean hours music (Z).'", 39: 'Rapid-fire revision: in timed conditions, tackle questions you are MOST confident about first. Every mark counts — a simple BEMDAS question is worth the same as a hard algebra question.', 40: "Geometry revision: know what's in the Formulae & Tables booklet: trig ratios, Sine Rule, Cosine Rule, area, volume formulae. Never memorise what is given to you in the exam.", 41: 'Statistics revision: the most common lost marks are: median without ordering; IQR confused with range; line of best fit not through mean point; conditional probability wrong denominator.', 42: 'Mock Paper 1: time management — 8–10 minutes per question. If stuck after 3 minutes, write the formula and move on. Return at the end. A formula alone earns the method mark.', 43: 'Mock Paper 2: geometry rewards neat diagrams. Draw large, clear figures with all measurements labelled. Statistics: always show your frequency table BEFORE calculating the mean.', 44: 'Full mock: the real SEC paper has 10 questions with 3 parts each. Parts (a) and (b) are usually accessible — secure those first. Attempt part (c) for method marks even if unsure.', 45: 'Exam day: open the Formulae & Tables booklet at the start and flag the pages you use most: area/volume formulae, trig, sequences, statistics. Everything you need is there.'}
for _d in DAYS:
    _d['tip'] = _TIPS.get(_d['day'], 'Show all working clearly. Method marks are awarded even when arithmetic errors occur.')


# ─── USERS CONFIG ─────────────────────────────────────────────────────────────
STUDENTS = [
    {"key": "reya",    "name": "Reya",    "pin": "1234"},
    {"key": "arnav",   "name": "Arnav",   "pin": "2345"},
    {"key": "sanjith", "name": "Sanjith", "pin": "3456"},
]
PARENTS = [
    {"key": "peppin", "name": "Peppin", "pin": "9001", "child_key": "reya",    "child_name": "Reya"},
    {"key": "viren",  "name": "Viren",  "pin": "9002", "child_key": "arnav",   "child_name": "Arnav"},
    {"key": "muthu",  "name": "Muthu",  "pin": "9003", "child_key": "sanjith", "child_name": "Sanjith"},
]

AUTH_GUARD = """
<script>
(function(){
  var sess=JSON.parse(sessionStorage.getItem('ptc_session')||'null');
  if(!sess){location.replace('login.html');return;}
  if(sess.role==='parent'){location.replace('parent.html');return;}
  var el=document.getElementById('nav-student-name');
  if(el)el.textContent=sess.name;
})();
</script>
"""

PARENT_GUARD = """
<script>
(function(){
  var sess=JSON.parse(sessionStorage.getItem('ptc_session')||'null');
  if(!sess){location.replace('login.html');return;}
  if(sess.role==='student'){location.replace('index.html');return;}
})();
</script>
"""

def nav_bar(active="home"):
    links = [
        ("home",     "index.html",    "🏠 Home"),
        ("plan",     "plan.html",     "📅 45-Day Plan"),
        ("quiz",     "quiz.html",     "⚡ Quick Quiz"),
        ("progress", "progress.html", "📈 My Progress"),
    ]
    items = ""
    for key, href, label in links:
        cls = "active" if key == active else ""
        items += f'<a href="{href}" class="nav-link {cls}">{label}</a>\n'
    return f"""<nav class="navbar">
  <div class="nav-brand">
    <span class="nav-logo">🍀</span>
    <div>
      <div class="nav-title">Peppin's Maths</div>
      <div class="nav-sub">Junior Cycle · First Year</div>
    </div>
  </div>
  <div class="nav-links">{items}</div>
  <div style="display:flex;align-items:center;gap:.5rem;margin-left:auto;">
    <span id="nav-student-name" style="font-size:.78rem;font-weight:700;color:var(--navy);padding:.3rem .6rem;background:#EEF2FF;border-radius:8px;white-space:nowrap;"></span>
    <button onclick="doLogout()" class="btn btn-sm" style="background:#fee2e2;color:#991b1b;border:none;cursor:pointer;">🚪 Logout</button>
  </div>
  <button class="nav-toggle" onclick="document.querySelector('.nav-links').classList.toggle('open')">☰</button>
</nav>
<script>
function doLogout(){{
  sessionStorage.removeItem('ptc_session');
  location.replace('login.html');
}}
var _s=JSON.parse(sessionStorage.getItem('ptc_session')||'null');
if(_s){{var el=document.getElementById('nav-student-name');if(el)el.textContent=_s.name;}}
</script>"""


# ─── LOGIN PAGE ───────────────────────────────────────────────────────────────
def generate_login():
    students_json = json.dumps([{"key": s["key"], "name": s["name"], "pin": s["pin"]} for s in STUDENTS])
    parents_json  = json.dumps([{"key": p["key"], "name": p["name"], "pin": p["pin"],
                                  "child_key": p["child_key"], "child_name": p["child_name"]} for p in PARENTS])
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Login · Peppin's Tuition Centre</title>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;800;900&family=Merriweather:wght@700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
<style>
body{{display:flex;align-items:center;justify-content:center;min-height:100vh;background:linear-gradient(135deg,#1B3A6B 0%,#2d5496 60%,#2E7D32 100%);padding:1rem;}}
.login-card{{background:#fff;border-radius:20px;padding:2.5rem 2rem;width:100%;max-width:420px;box-shadow:0 20px 60px rgba(0,0,0,.25);}}
.login-logo{{text-align:center;margin-bottom:1.5rem;}}
.login-logo .emoji{{font-size:3rem;}}
.login-logo h1{{font-family:'Merriweather',serif;font-size:1.4rem;color:#1B3A6B;margin:.4rem 0 .2rem;}}
.login-logo p{{font-size:.82rem;color:#6B7280;}}
.tab-row{{display:flex;gap:.4rem;background:#F3F4F6;border-radius:10px;padding:.3rem;margin-bottom:1.5rem;}}
.tab-btn{{flex:1;padding:.55rem;border:none;border-radius:8px;font-family:'Nunito',sans-serif;font-weight:700;font-size:.88rem;cursor:pointer;transition:all .2s;background:transparent;color:#6B7280;}}
.tab-btn.active{{background:#fff;color:#1B3A6B;box-shadow:0 1px 4px rgba(0,0,0,.1);}}
.form-group{{margin-bottom:1rem;}}
label{{display:block;font-weight:700;font-size:.85rem;margin-bottom:.4rem;color:#374151;}}
select,input[type=password]{{width:100%;padding:.75rem 1rem;border:2px solid #E5E7EB;border-radius:10px;font-family:'Nunito',sans-serif;font-size:.95rem;font-weight:600;outline:none;transition:border .2s;}}
select:focus,input:focus{{border-color:#1B3A6B;}}
.pin-row{{display:flex;gap:.5rem;justify-content:center;margin:.5rem 0;}}
.pin-digit{{width:52px;height:60px;border:2px solid #E5E7EB;border-radius:12px;font-size:1.6rem;font-weight:900;text-align:center;font-family:'Nunito',sans-serif;outline:none;transition:border .2s;}}
.pin-digit:focus{{border-color:#1B3A6B;}}
.btn-login{{width:100%;padding:.85rem;background:#1B3A6B;color:#fff;border:none;border-radius:12px;font-family:'Nunito',sans-serif;font-size:1rem;font-weight:800;cursor:pointer;transition:background .2s;margin-top:.5rem;}}
.btn-login:hover{{background:#2d5496;}}
.error-msg{{background:#FEE2E2;color:#991B1B;border-radius:8px;padding:.65rem 1rem;font-size:.85rem;font-weight:700;margin-top:.75rem;display:none;text-align:center;}}
</style>
</head>
<body>
<div class="login-card">
  <div class="login-logo">
    <div class="emoji">🍀</div>
    <h1>Peppin's Tuition Centre</h1>
    <p>Junior Cycle Mathematics · Cork</p>
  </div>

  <div class="tab-row">
    <button class="tab-btn active" onclick="switchRole('student',this)">👩‍🎓 Student</button>
    <button class="tab-btn" onclick="switchRole('parent',this)">👨‍👧 Parent</button>
  </div>

  <div id="student-form">
    <div class="form-group">
      <label>Who are you?</label>
      <select id="student-select">
        <option value="">— Select your name —</option>
        <option value="reya">Reya</option>
        <option value="arnav">Arnav</option>
        <option value="sanjith">Sanjith</option>
      </select>
    </div>
    <div class="form-group">
      <label>Enter your PIN</label>
      <div class="pin-row">
        <input class="pin-digit" id="s0" maxlength="1" type="password" inputmode="numeric" oninput="moveFocus(this,'s1')">
        <input class="pin-digit" id="s1" maxlength="1" type="password" inputmode="numeric" oninput="moveFocus(this,'s2')">
        <input class="pin-digit" id="s2" maxlength="1" type="password" inputmode="numeric" oninput="moveFocus(this,'s3')">
        <input class="pin-digit" id="s3" maxlength="1" type="password" inputmode="numeric" onkeyup="if(event.key==='Enter')doLogin()">
      </div>
    </div>
    <button class="btn-login" onclick="doLogin()">Login →</button>
  </div>

  <div id="parent-form" style="display:none">
    <div class="form-group">
      <label>Who are you?</label>
      <select id="parent-select">
        <option value="">— Select your name —</option>
        <option value="peppin">Peppin (Reya's Dad)</option>
        <option value="viren">Viren (Arnav's Dad)</option>
        <option value="muthu">Muthu (Sanjith's Dad)</option>
      </select>
    </div>
    <div class="form-group">
      <label>Enter your PIN</label>
      <div class="pin-row">
        <input class="pin-digit" id="p0" maxlength="1" type="password" inputmode="numeric" oninput="moveFocus(this,'p1')">
        <input class="pin-digit" id="p1" maxlength="1" type="password" inputmode="numeric" oninput="moveFocus(this,'p2')">
        <input class="pin-digit" id="p2" maxlength="1" type="password" inputmode="numeric" oninput="moveFocus(this,'p3')">
        <input class="pin-digit" id="p3" maxlength="1" type="password" inputmode="numeric" onkeyup="if(event.key==='Enter')doLogin()">
      </div>
    </div>
    <button class="btn-login" onclick="doLogin()">Login →</button>
  </div>

  <div class="error-msg" id="error-msg">❌ Incorrect name or PIN. Please try again.</div>
</div>

<script>
const STUDENTS = {students_json};
const PARENTS  = {parents_json};
let currentRole = 'student';

function switchRole(role, btn){{
  currentRole = role;
  document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  document.getElementById('student-form').style.display = role==='student'?'block':'none';
  document.getElementById('parent-form').style.display  = role==='parent' ?'block':'none';
  document.getElementById('error-msg').style.display='none';
}}

function moveFocus(el, nextId){{
  if(el.value.length===1){{
    var next=document.getElementById(nextId);
    if(next) next.focus();
  }}
}}

function getPin(prefix){{
  return ['0','1','2','3'].map(i=>document.getElementById(prefix+i).value).join('');
}}

function doLogin(){{
  document.getElementById('error-msg').style.display='none';
  if(currentRole==='student'){{
    var key=document.getElementById('student-select').value;
    var pin=getPin('s');
    var match=STUDENTS.find(s=>s.key===key && s.pin===pin);
    if(match){{
      sessionStorage.setItem('ptc_session', JSON.stringify({{role:'student',key:match.key,name:match.name}}));
      location.replace('index.html');
    }} else {{
      document.getElementById('error-msg').style.display='block';
      ['s0','s1','s2','s3'].forEach(id=>document.getElementById(id).value='');
      document.getElementById('s0').focus();
    }}
  }} else {{
    var key=document.getElementById('parent-select').value;
    var pin=getPin('p');
    var match=PARENTS.find(p=>p.key===key && p.pin===pin);
    if(match){{
      sessionStorage.setItem('ptc_session', JSON.stringify({{role:'parent',key:match.key,name:match.name,child_key:match.child_key,child_name:match.child_name}}));
      location.replace('parent.html');
    }} else {{
      document.getElementById('error-msg').style.display='block';
      ['p0','p1','p2','p3'].forEach(id=>document.getElementById(id).value='');
      document.getElementById('p0').focus();
    }}
  }}
}}

// If already logged in, skip login page
var existing = JSON.parse(sessionStorage.getItem('ptc_session')||'null');
if(existing){{
  location.replace(existing.role==='parent'?'parent.html':'index.html');
}}
</script>
</body></html>"""


# ─── PARENT DASHBOARD ─────────────────────────────────────────────────────────
def generate_parent():
    day_topics_json = json.dumps({d["day"]: d["topic"] for d in DAYS})
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Parent Dashboard · Peppin's Tuition Centre</title>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;800;900&family=Merriweather:wght@700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head>
<body>
{PARENT_GUARD}
<nav class="navbar">
  <div class="nav-brand">
    <span class="nav-logo">🍀</span>
    <div>
      <div class="nav-title">Peppin's Maths</div>
      <div class="nav-sub">Parent Dashboard</div>
    </div>
  </div>
  <div style="margin-left:auto;display:flex;align-items:center;gap:.75rem;">
    <span id="parent-greeting" style="font-size:.85rem;font-weight:700;color:var(--navy);"></span>
    <button onclick="sessionStorage.removeItem('ptc_session');location.replace('login.html');" class="btn btn-sm" style="background:#fee2e2;color:#991b1b;border:none;cursor:pointer;">🚪 Logout</button>
  </div>
</nav>

<div style="background:linear-gradient(135deg,var(--navy),#2d5496);color:#fff;padding:2rem 1.5rem;">
  <div style="max-width:900px;margin:0 auto;">
    <div style="font-size:2rem;margin-bottom:.5rem">👨‍👧</div>
    <h1 id="dashboard-title" style="font-family:'Merriweather',serif;font-size:1.6rem;margin-bottom:.3rem;"></h1>
    <p id="dashboard-sub" style="opacity:.8;font-size:.9rem;"></p>
  </div>
</div>

<div class="container" style="max-width:900px;">
  <div class="stats-strip mt3">
    <div class="stat-box"><div class="stat-num" id="p-days-done" style="color:var(--navy)">0</div><div class="stat-label">Days Complete</div></div>
    <div class="stat-box"><div class="stat-num" id="p-pct" style="color:var(--green)">0%</div><div class="stat-label">Progress</div></div>
    <div class="stat-box"><div class="stat-num" id="p-days-left" style="color:var(--gold)">45</div><div class="stat-label">Days Remaining</div></div>
  </div>

  <div class="card mt3" style="padding:1.25rem;">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:.75rem;">
      <strong id="progress-title">Progress</strong>
      <span id="p-overall-label" style="color:var(--muted);font-size:.85rem;"></span>
    </div>
    <div class="progress-bar" style="height:14px;">
      <div class="progress-fill" id="p-overall-fill" style="background:linear-gradient(90deg,var(--navy),var(--green));width:0%"></div>
    </div>
  </div>

  <h3 style="margin:1.5rem 0 .75rem;font-family:'Merriweather',serif;">Day-by-Day Progress</h3>
  <p class="muted mb2" style="font-size:.85rem;">✅ = completed · 📖 = not yet started</p>
  <div id="p-day-tracker" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(90px,1fr));gap:.5rem;"></div>

  <div class="card mt4" style="padding:1.25rem;background:#FFF8E1;border-left:4px solid var(--gold);">
    <strong>📌 Note for Parents</strong>
    <p style="font-size:.88rem;margin-top:.4rem;color:#555;">This view shows your child's progress as stored on <em>their device</em>. Progress is saved automatically each time they mark a day complete. If your child uses a different device, progress may differ.</p>
  </div>
</div>

<footer style="background:var(--navy);color:rgba(255,255,255,.7);text-align:center;padding:1.5rem;font-size:.82rem;margin-top:3rem;">
  <strong style="color:#fff">Peppin's Tuition Centre, Cork</strong> · Parent Dashboard · Junior Cycle Mathematics
</footer>

<script>
const DAY_TOPICS = {day_topics_json};

function loadParentDashboard(){{
  var sess = JSON.parse(sessionStorage.getItem('ptc_session')||'null');
  if(!sess || sess.role!=='parent') return;

  document.getElementById('parent-greeting').textContent = 'Hi, ' + sess.name + '!';
  document.getElementById('dashboard-title').textContent = sess.child_name + "'s Progress Dashboard";
  document.getElementById('dashboard-sub').textContent = "Viewing " + sess.child_name + "'s Junior Cycle Maths journey";
  document.getElementById('progress-title').textContent = sess.child_name + "'s Overall Progress";

  // Read child's localStorage — parent must be on same device OR child shares device
  // Progress keys are prefixed with child's key
  var childKey = sess.child_key;
  var done = 0;
  var total = 45;
  var html = '';

  for(var i=1; i<=total; i++){{
    var complete = !!localStorage.getItem('day_complete_' + childKey + '_' + i);
    if(complete) done++;
    var topic = DAY_TOPICS[i] || '';
    html += '<div title="Day '+i+': '+topic+'" style="display:flex;flex-direction:column;align-items:center;justify-content:center;background:'+(complete?'var(--green)':'#fff')+';color:'+(complete?'#fff':'var(--text)')+';border:2px solid '+(complete?'var(--green)':'var(--border)')+';border-radius:10px;padding:.5rem .25rem;font-weight:800;font-size:.82rem;text-align:center;">'
      + '<span style="font-size:1.1rem">'+(complete?'✅':'📖')+'</span>'
      + '<span>Day '+i+'</span>'
      + '</div>';
  }}

  document.getElementById('p-day-tracker').innerHTML = html;
  document.getElementById('p-days-done').textContent = done;
  document.getElementById('p-pct').textContent = Math.round(done/total*100) + '%';
  document.getElementById('p-days-left').textContent = total - done;
  document.getElementById('p-overall-label').textContent = done + ' / ' + total + ' days';
  document.getElementById('p-overall-fill').style.width = Math.round(done/total*100) + '%';
}}

loadParentDashboard();
</script>
</body></html>"""


# ─── UPDATED GENERATE_PROGRESS (student-scoped storage) ──────────────────────
def generate_progress():
    day_topics_json = json.dumps({d["day"]: d["topic"] for d in DAYS})
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>My Progress · Peppin's Maths</title>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;800;900&family=Merriweather:wght@700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head>
<body>
{AUTH_GUARD}
{nav_bar("progress")}
<div class="page-hero">
  <h1>📈 My Progress</h1>
  <p id="progress-sub">Track your journey through the 45-day programme</p>
</div>
<div class="container" style="max-width:900px;">
  <div class="stats-strip mt3">
    <div class="stat-box"><div class="stat-num" id="days-done" style="color:var(--navy)">0</div><div class="stat-label">Days Complete</div></div>
    <div class="stat-box"><div class="stat-num" id="pct-done" style="color:var(--green)">0%</div><div class="stat-label">Progress</div></div>
    <div class="stat-box"><div class="stat-num" id="days-left" style="color:var(--gold)">45</div><div class="stat-label">Days Remaining</div></div>
  </div>
  <div class="card mt3" style="padding:1.25rem;">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:.75rem;">
      <strong>Overall Progress</strong>
      <span id="overall-label" style="color:var(--muted);font-size:.85rem">0 / 45 days</span>
    </div>
    <div class="progress-bar" style="height:14px"><div class="progress-fill" id="overall-fill" style="background:linear-gradient(90deg,var(--navy),var(--green))"></div></div>
  </div>
  <h3 style="margin:1.5rem 0 .75rem;font-family:'Merriweather',serif;">Day-by-Day Tracker</h3>
  <div id="day-tracker" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(90px,1fr));gap:.5rem;"></div>
  <div style="text-align:center;margin-top:2rem;">
    <button class="btn btn-red" onclick="resetProgress()">🗑️ Reset My Progress</button>
  </div>
</div>
<footer style="background:var(--navy);color:rgba(255,255,255,.7);text-align:center;padding:1.5rem;font-size:.82rem;margin-top:3rem;">
  <strong style="color:#fff">Peppin's Tuition Centre, Cork</strong> · Junior Cycle Mathematics Progress Tracker
</footer>
<script>
const DAY_TOPICS = {day_topics_json};

function getStudentKey(){{
  var sess = JSON.parse(sessionStorage.getItem('ptc_session')||'null');
  return sess ? sess.key : null;
}}

function storageKey(day){{
  return 'day_complete_' + getStudentKey() + '_' + day;
}}

function loadProgress(){{
  var sess = JSON.parse(sessionStorage.getItem('ptc_session')||'null');
  if(sess) document.getElementById('progress-sub').textContent = sess.name + "'s journey through the 45-day programme";

  var done=0, total=45, html='';
  for(var i=1;i<=total;i++){{
    var complete=!!localStorage.getItem(storageKey(i));
    if(complete) done++;
    var topic=DAY_TOPICS[i]||'';
    html+='<a href="day'+i+'.html" title="Day '+i+': '+topic+'" style="display:flex;flex-direction:column;align-items:center;justify-content:center;background:'+(complete?'var(--green)':'#fff')+';color:'+(complete?'#fff':'var(--text)')+';border:2px solid '+(complete?'var(--green)':'var(--border)')+';border-radius:10px;padding:.5rem .25rem;font-weight:800;font-size:.82rem;text-decoration:none;">'
      +'<span style="font-size:1.1rem">'+(complete?'✅':'📖')+'</span>'
      +'<span>Day '+i+'</span>'
      +'</a>';
  }}
  document.getElementById('day-tracker').innerHTML=html;
  document.getElementById('days-done').textContent=done;
  document.getElementById('pct-done').textContent=Math.round(done/total*100)+'%';
  document.getElementById('days-left').textContent=total-done;
  document.getElementById('overall-label').textContent=done+' / '+total+' days';
  document.getElementById('overall-fill').style.width=Math.round(done/total*100)+'%';
}}

function resetProgress(){{
  if(confirm('Reset all your progress? This cannot be undone.')){{
    var k=getStudentKey();
    for(var i=1;i<=45;i++) localStorage.removeItem('day_complete_'+k+'_'+i);
    loadProgress();
  }}
}}

loadProgress();
</script>
</body></html>"""


# ─── UPDATED GENERATE_INDEX (student-scoped marks) ────────────────────────────
def generate_index():
    block_sections = {}
    for d in DAYS:
        b = d["block"]
        block_sections.setdefault(b, []).append(d)

    hero = f"""
{nav_bar("home")}
<div class="page-hero">
  <div style="font-size:2.5rem;margin-bottom:.5rem">📐 🔢 📊</div>
  <h1>Junior Cycle Mathematics</h1>
  <p id="hero-sub">Peppin's Tuition Centre, Cork · First Year · 45-Day Study Programme</p>
  <div style="display:flex;gap:.75rem;justify-content:center;flex-wrap:wrap;margin-top:1.25rem;">
    <a href="plan.html" class="btn btn-gold btn-lg">📅 View 45-Day Plan</a>
    <a href="quiz.html" class="btn btn-primary btn-lg" style="background:rgba(255,255,255,.15);border:2px solid rgba(255,255,255,.4);">⚡ Quick Quiz</a>
  </div>
</div>
"""
    stats = f"""
<div class="container">
  <div class="stats-strip">
    <div class="stat-box"><div class="stat-num" style="color:var(--navy)">45</div><div class="stat-label">Study Days</div></div>
    <div class="stat-box"><div class="stat-num" style="color:var(--green)">5</div><div class="stat-label">Topic Blocks</div></div>
    <div class="stat-box"><div class="stat-num" style="color:var(--gold)">{sum(len(d['questions']) for d in DAYS)}</div><div class="stat-label">Practice Questions</div></div>
    <div class="stat-box"><div class="stat-num" style="color:var(--red)">{len(DAYS)}</div><div class="stat-label">Lessons</div></div>
  </div>
"""

    content = ""
    for block_name, block_days in block_sections.items():
        info = BLOCKS.get(block_name, {"color":"#555","icon":"📚"})
        color = info["color"]
        icon = info["icon"]
        content += f"""
  <div class="mt4">
    <div style="display:flex;align-items:center;gap:.75rem;margin-bottom:1rem;padding-bottom:.6rem;border-bottom:3px solid {color};">
      <span style="font-size:1.5rem">{icon}</span>
      <div>
        <h2 style="font-family:'Merriweather',serif;color:{color};font-size:1.25rem;">{block_name}</h2>
        <div style="font-size:.8rem;color:var(--muted);">Days {block_days[0]['day']}–{block_days[-1]['day']}</div>
      </div>
    </div>
    <div class="grid-3">
"""
        for d in block_days:
            lc = level_color(d["level"])
            content += f"""
      <a href="day{d['day']}.html" class="card day-card" style="border-left-color:{d['color']}">
        <div class="card-header" style="padding:.75rem 1rem;">
          <div>
            <div class="day-num" style="color:{d['color']}">Day {d['day']}</div>
            <div class="day-topic">{d['topic']}</div>
            <div class="day-sub">{d['subtopic']}</div>
            <div class="day-meta">
              <span class="level-badge" style="background:{lc}">{d['level']}</span>
              <span style="font-size:.72rem;color:var(--muted)">{len(d['questions'])} questions</span>
              <span class="completed-mark" id="mark-{d['day']}"></span>
            </div>
          </div>
        </div>
      </a>
"""
        content += "    </div>\n  </div>\n"

    footer = """
  <footer style="background:var(--navy);color:rgba(255,255,255,.7);text-align:center;padding:1.5rem;font-size:.82rem;margin-top:3rem;">
    <strong style="color:#fff">Peppin's Tuition Centre, Cork</strong> · Junior Cycle Mathematics · 45-Day Tuition Programme
  </footer>
"""
    script = """
<script>
// Auth guard
(function(){
  var sess=JSON.parse(sessionStorage.getItem('ptc_session')||'null');
  if(!sess){location.replace('login.html');return;}
  if(sess.role==='parent'){location.replace('parent.html');return;}
  // personalise
  document.getElementById('hero-sub').textContent=sess.name+"'s Junior Cycle Maths · Peppin's Tuition Centre, Cork";
  var el=document.getElementById('nav-student-name');if(el)el.textContent=sess.name;
  // load completion marks scoped to this student
  document.querySelectorAll('[id^="mark-"]').forEach(function(el){
    var day=el.id.replace('mark-','');
    if(localStorage.getItem('day_complete_'+sess.key+'_'+day)) el.textContent='✅';
  });
})();
</script>
"""
    return html_head("Peppin's Maths · Home") + "<body>" + AUTH_GUARD + hero + stats + content + "</div>" + footer + script + "</body></html>"


# ─── UPDATED GENERATE_DAY_PAGE (student-scoped markComplete) ─────────────────
def generate_day_page(d):
    day_num = d["day"]
    lc = level_color(d["level"])
    c = d["concept"]

    explains = "".join(f"<p>{p}</p>" for p in c["explain"])
    mistakes = "".join(f"<li>{m}</li>" for m in c["mistakes"])
    formulae = "".join(f"<code>{f}</code>" for f in c["formulae"])
    steps    = "".join(f"<li>{s}</li>" for s in c["worked"]["steps"])

    concept_html = f"""
<div class="tab-content active" id="tab-concept">
  <div class="concept-section mt2">
    <div class="section-label" style="color:#1565C0">📘 What is this topic?</div>
    <div class="explain-box">{explains}</div>
  </div>
  <div class="concept-section">
    <div class="section-label" style="color:var(--gold)">💡 Analogy — How to picture it</div>
    <div class="analogy-box"><p>{c['analogy']}</p></div>
  </div>
  <div class="concept-section">
    <div class="section-label" style="color:var(--green)">🔍 Worked Example</div>
    <div class="worked-box">
      <strong style="display:block;margin-bottom:.6rem">{c['worked']['title']}</strong>
      <ol class="step-list">{steps}</ol>
    </div>
  </div>
  <div class="concept-section">
    <div class="section-label" style="color:#BF360C">⚠️ Common Mistakes</div>
    <div class="mistake-box"><ul style="padding-left:1.2rem">{mistakes}</ul></div>
  </div>
  <div class="concept-section">
    <div class="section-label" style="color:var(--navy)">📌 Key Formulae</div>
    <div class="formula-box">{formulae}</div>
  </div>
  <div class="tip-box mt2">
    <strong>🎯 SEC Exam Insight:</strong> {d.get('tip','')}
  </div>
</div>
"""

    q_html = '<div class="tab-content" id="tab-questions">\n'
    for q in d["questions"]:
        q_html += f"""
<div class="question-card">
  <div class="q-header">
    <span class="q-num">Q{q['q']}</span>
    <span style="flex:1;font-size:.9rem">{q['text']}</span>
    <span class="q-marks">{q['marks']} mark{'s' if q['marks']>1 else ''}</span>
  </div>
  <div class="q-hint" id="hint-{day_num}-{q['q']}">💡 <em>{q['hint']}</em></div>
  <div class="q-answer" id="ans-{day_num}-{q['q']}"><strong>✅ Answer:</strong> {q['answer']}</div>
  <div class="q-actions">
    <button class="btn btn-hint btn-sm" onclick="toggleEl('hint-{day_num}-{q['q']}')">💡 Hint</button>
    <button class="btn btn-answer btn-sm" onclick="toggleEl('ans-{day_num}-{q['q']}')">✅ Show Answer</button>
  </div>
</div>
"""
    q_html += "</div>\n"

    prev_link = f'<a href="day{day_num-1}.html" class="btn btn-primary">← Day {day_num-1}</a>' if day_num > 1 else ""
    next_link = f'<a href="day{day_num+1}.html" class="btn btn-green">Day {day_num+1} →</a>' if day_num < 45 else ""

    body = f"""
{AUTH_GUARD}
{nav_bar()}
<div style="background:{d['color']};color:#fff;padding:1.5rem 1.5rem 1rem;">
  <div style="max-width:900px;margin:0 auto;">
    <a href="index.html" style="color:rgba(255,255,255,.7);font-size:.82rem;font-weight:700;">← Back to Home</a>
    <div style="display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:1rem;margin-top:.6rem;">
      <div>
        <div style="font-size:.75rem;opacity:.7;font-weight:800;letter-spacing:.1em;text-transform:uppercase;">Day {day_num} of 45 · {d['block']}</div>
        <h1 style="font-family:'Merriweather',serif;font-size:clamp(1.3rem,3vw,2rem);margin:.3rem 0;">{d['topic']}</h1>
        <div style="font-size:1rem;opacity:.85;">{d['subtopic']}</div>
        <div style="margin-top:.6rem;display:flex;gap:.5rem;flex-wrap:wrap;align-items:center;">
          <span class="level-badge" style="background:rgba(255,255,255,.2);border:1px solid rgba(255,255,255,.4)">{d['level']}</span>
          <span style="font-size:.78rem;opacity:.7">{len(d['questions'])} questions · {sum(q['marks'] for q in d['questions'])} marks total</span>
        </div>
      </div>
      <div style="text-align:center;">
        <div style="font-size:2.5rem;line-height:1">{'🔢' if d['block']=='Number' else '✖️' if d['block']=='Algebra' else '📐' if d['block']=='Geometry' else '📊' if d['block']=='Statistics' else '📝'}</div>
      </div>
    </div>
  </div>
</div>

<div class="container" style="max-width:900px;">
  <div class="tab-bar">
    <button class="tab active" onclick="switchTab('concept',this)">📖 Concept</button>
    <button class="tab" onclick="switchTab('questions',this)">✏️ Practice Questions</button>
  </div>
  {concept_html}
  {q_html}
  <div style="display:flex;gap:.75rem;justify-content:space-between;flex-wrap:wrap;margin-top:2rem;padding-top:1rem;border-top:2px solid var(--border);">
    {prev_link}
    <button class="btn btn-gold" id="complete-btn" onclick="markComplete({day_num})">✅ Mark Day {day_num} Complete</button>
    {next_link}
  </div>
</div>

<footer style="background:var(--navy);color:rgba(255,255,255,.7);text-align:center;padding:1.5rem;font-size:.82rem;margin-top:3rem;">
  <strong style="color:#fff">Peppin's Tuition Centre, Cork</strong> · Day {day_num} · {d['topic']}
</footer>

<script>
function switchTab(name,btn){{
  document.querySelectorAll('.tab-content').forEach(t=>t.classList.remove('active'));
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
  document.getElementById('tab-'+name).classList.add('active');
  btn.classList.add('active');
}}
function toggleEl(id){{
  var el=document.getElementById(id);
  el.style.display=el.style.display==='block'?'none':'block';
}}
function getStudentKey(){{
  var sess=JSON.parse(sessionStorage.getItem('ptc_session')||'null');
  return sess?sess.key:null;
}}
function markComplete(day){{
  var k=getStudentKey();
  if(!k) return;
  localStorage.setItem('day_complete_'+k+'_'+day,'1');
  var btn=document.getElementById('complete-btn');
  btn.textContent='🎉 Day '+day+' Complete!';
  btn.style.background='var(--green)';
  btn.disabled=true;
}}
// Check if already complete
(function(){{
  var k=getStudentKey();
  if(k && localStorage.getItem('day_complete_'+k+'_{day_num}')){{
    var btn=document.getElementById('complete-btn');
    if(btn){{btn.textContent='🎉 Day {day_num} Complete!';btn.style.background='var(--green)';btn.disabled=true;}}
  }}
}})();
</script>
"""
    return html_head(f"Day {day_num} · {d['topic']} · Peppin's Maths") + "<body>" + body + "</body></html>"


# ─── BUILD ────────────────────────────────────────────────────────────────────
def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    print("🔨 Building Peppin's Tuition Centre Maths App (with multi-user auth)...")

    (OUT / "style.css").write_text(generate_css(), encoding="utf-8")
    print("  ✅ style.css")

    (OUT / "login.html").write_text(generate_login(), encoding="utf-8")
    print("  ✅ login.html  (students + parents)")

    (OUT / "parent.html").write_text(generate_parent(), encoding="utf-8")
    print("  ✅ parent.html  (Peppin / Viren / Muthu)")

    (OUT / "index.html").write_text(generate_index(), encoding="utf-8")
    print("  ✅ index.html")

    (OUT / "plan.html").write_text(generate_plan(), encoding="utf-8")
    print("  ✅ plan.html")

    (OUT / "quiz.html").write_text(generate_quiz(), encoding="utf-8")
    print("  ✅ quiz.html")

    (OUT / "progress.html").write_text(generate_progress(), encoding="utf-8")
    print("  ✅ progress.html")

    for d in DAYS:
        (OUT / f"day{d['day']}.html").write_text(generate_day_page(d), encoding="utf-8")
    print(f"  ✅ {len(DAYS)} day pages")

    Path("README.md").write_text(generate_readme(), encoding="utf-8")
    print("  ✅ README.md")

    (OUT / "404.html").write_text(generate_404(), encoding="utf-8")
    print("  ✅ 404.html")

    (OUT / ".nojekyll").write_text("", encoding="utf-8")

    total_files = len(list(OUT.iterdir()))
    total_size  = sum(f.stat().st_size for f in OUT.iterdir() if f.is_file())
    print(f"\n🎉 Done! {total_files} files · {total_size//1024} KB total")
    print(f"\n📋 LOGIN CREDENTIALS:")
    print(f"  STUDENTS         PIN")
    for s in STUDENTS:
        print(f"  {s['name']:<16} {s['pin']}")
    print(f"\n  PARENTS          PIN   (sees child's progress)")
    for p in PARENTS:
        print(f"  {p['name']:<16} {p['pin']}   → {p['child_name']}")
    print(f"\n  ⚠️  Change PINs in the STUDENTS / PARENTS section at the top of generate.py")
    print(f"\nTo preview:  cd docs && python3 -m http.server 8080\n")


if __name__ == "__main__":
    build()

