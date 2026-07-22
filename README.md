# Discrete-Mathematics-Visualization-Engine

I engineered this Python animation tool to generate dynamic visual proofs for Discrete Mathematics. Sometimes, reading mathematical proofs isn't enough to make the concepts "click." By animating the logic, this project produces a visual lecture designed to help future students intuitively grasp Euler's Totient Function and its foundation in the Principle of Inclusion and Exclusion.

## What's Inside?

This project leverages the `manim` library to programmatically generate mathematical animations. Key features include:

* **Custom Animated Mascot:** Features a custom `PhiCharacter` class—an animated $\varphi$ symbol with randomized blinking and dynamic eye-tracking that actively looks at the formulas being presented to guide the viewer's attention.


* **Set Theory Visuals:** Creates clean, animated Venn diagrams for 2-set and 3-set scenarios to visually introduce the Principle of Inclusion and Exclusion using custom color palettes.


* **Step-by-Step LaTeX Rendering:** Smoothly animates the mathematical progression from the general inclusion-exclusion formula to the specific prime factorization of $n$.


* **Logical Proof Construction:** Visually substitutes set sizes (e.g., $\vert{}A_i\vert{}=\frac{n}{p_i}$) to map out the algebra, ultimately arriving at the final product formula: $\varphi(n)=n\prod_{i=1}^{k}\left(1-\frac{1}{p_i}\right)$.


* **Practical Examples:** Concludes the abstract proof with a concrete, animated example calculating $\varphi(4) = 2$.



## Tech Stack

* `manim` (For mathematical typesetting and scene rendering)


* `numpy` (For calculating eye-tracking vectors and vector normalization)


* `random` (For generating organic, randomized blink intervals for the mascot)



## How to Run It

1. Ensure you have Python installed along with the [Manim library](https://www.manim.community/) and its system dependencies (like FFmpeg and LaTeX).
2. Clone this repository to your local machine.
3. Open your terminal, navigate to the project directory, and run the following command to render the animation:
`manim -pql main.py math`
*(Note: `-pql` renders it in low quality for a quick preview. Use `-pqh` for high quality).*
4. The generated video file will automatically play once the rendering is complete!
