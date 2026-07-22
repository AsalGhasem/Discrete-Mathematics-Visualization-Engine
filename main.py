from manim import *
import random 
import numpy as np

MY_GREEN  = "#9bdeac"
MY_PINK   = "#c197e2"
MY_YELLOW = "#e7e1a2"
MY_BLUE    = "#4f9de0"

class PhiCharacter(VGroup):
    def __init__(self, color=MY_GREEN, scale_factor=5, **kwargs):
        super().__init__(**kwargs)

        self.phi = MathTex(r"\varphi", color=color)
        self.phi.scale(scale_factor)

        eye_radius = 0.15
        pupil_radius = 0.06

        self.left_eye = Dot(radius=eye_radius, color=WHITE)
        self.right_eye = Dot(radius=eye_radius, color=WHITE)
        self.left_pupil = Dot(radius=pupil_radius, color=BLACK)
        self.right_pupil = Dot(radius=pupil_radius, color=BLACK)

        self.left_eye_initial_height = self.left_eye.height
        self.right_eye_initial_height = self.right_eye.height

        self.left_eye.move_to(self.phi.get_center() + LEFT * 0.25 + UP * 0.01)
        self.right_eye.move_to(self.phi.get_center() + RIGHT * 0.25 + UP * 0.01)
        self.left_pupil.move_to(self.left_eye)
        self.right_pupil.move_to(self.right_eye)

        self.eyes = VGroup(
            self.left_eye,
            self.right_eye,
            self.left_pupil,
            self.right_pupil
        )

        self.add(self.phi, self.eyes)

        self.blink_timer = 0
        self.next_blink = random.uniform(2.5, 4.0)
        self.eyes_open = True

        # eye mode: "down", "viewer", "target"
        self.look_mode = "viewer"

        self.add_updater(PhiCharacter.behavior_updater)

    def look_at(self, target):
        self.look_mode = "target"
        self.target = target

    def look_back(self):
        self.look_mode = "viewer"

    @staticmethod
    def behavior_updater(mob, dt):
        mob.blink_timer += dt
        if mob.blink_timer > mob.next_blink and mob.eyes_open:
            mob.blink_timer = 0
            mob.next_blink = random.uniform(2.5, 4.0)
            mob.eyes_open = False

            for eye in [mob.left_eye, mob.right_eye]:
                eye.set_height(0.02)
            for pupil in [mob.left_pupil, mob.right_pupil]:
                pupil.set_opacity(0)

        if not mob.eyes_open and mob.blink_timer > 0.15:
            mob.eyes_open = True
            # restore to initial height
            mob.left_eye.set_height(mob.left_eye_initial_height)
            mob.right_eye.set_height(mob.right_eye_initial_height)
            for pupil in [mob.left_pupil, mob.right_pupil]:
                pupil.set_opacity(1)

        for eye, pupil in [
            (mob.left_eye, mob.left_pupil),
            (mob.right_eye, mob.right_pupil)
        ]:
            if mob.look_mode == "down":
                pupil.move_to(eye.get_center() + DOWN * 0.05)
            elif mob.look_mode == "viewer":
                pupil.move_to(eye.get_center())
            elif mob.look_mode == "target":
                direction = mob.target.get_center() - eye.get_center()
                norm = np.linalg.norm(direction)
                if norm != 0:
                    direction = direction / norm * 0.05
                pupil.move_to(eye.get_center() + direction)

class math(Scene):
    def construct(self):

        phi_char = PhiCharacter(color=MY_GREEN).to_corner(UL)
        self.add(phi_char) 

        phi_char2 = PhiCharacter(color= MY_PINK).to_corner(DR)
        self.add(phi_char2) 

        title = Text(
            "Proof of Euler’s Totient Function",
            font_size=48,
            weight=BOLD,
            color= MY_PINK,
            t2c={"Euler’s Totient Function": MY_GREEN},
            slant=ITALIC
        )

        subtitle = Text(
            "using the Principle of Inclusion and Exclusion",
            font_size=32,
            color= MY_PINK,
            t2c={"Inclusion and Exclusion": MY_GREEN},
            slant=ITALIC
        )
        subtitle.next_to(title, DOWN, buff=0.4)

        self.play(
            FadeIn(title, shift=UP),
            FadeIn(subtitle, shift=DOWN),
            run_time=1.5
        )
        self.play(
            UpdateFromFunc(phi_char, lambda m: m.look_at(subtitle)),
            run_time=1
        )
        self.wait(1)
        self.play(
            UpdateFromFunc(phi_char, lambda m: m.look_back()),
            run_time=1
        )
        self.play(
            UpdateFromFunc(phi_char2, lambda m: m.look_at(subtitle)),
            run_time=1
        )
        self.wait(1)
        self.play(
            UpdateFromFunc(phi_char2, lambda m: m.look_back()),
            run_time=1
        )
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle))

        # 2 sets (inclusion exclusion)
        A_text   = MathTex("A", color=MY_GREEN).move_to(ORIGIN + UP*1.125 + LEFT*5)
        B_text   = MathTex("B", color= MY_PINK).move_to(ORIGIN + DOWN*1.125 + LEFT*5)
        A_circle = Circle(color=MY_GREEN).move_to(ORIGIN + UP*1.125 + LEFT*3)
        B_circle = Circle(color= MY_PINK).move_to(ORIGIN + DOWN*1.125 + LEFT*3)

        self.play(Write(A_text), Write(B_text), Create(A_circle), Create(B_circle))
        self.wait(1)
        self.play(FadeOut(A_text, shift=RIGHT), FadeOut(A_circle, shift=RIGHT),
                  FadeOut(B_text, shift=LEFT), FadeOut(B_circle, shift=LEFT))

        A_circle_exin2 = Circle(color=MY_GREEN).move_to(ORIGIN + LEFT*0.45)
        B_circle_exin2 = Circle(color= MY_PINK).move_to(ORIGIN + RIGHT*0.45)
        exinformula_2 = MathTex(r"|A \cup B| = |A| + |B| - |A \cap B|", 
                                color= MY_YELLOW).move_to(ORIGIN + DOWN*2)

        self.play(Create(A_circle_exin2), Create(B_circle_exin2), Write(exinformula_2))
        self.wait(3)
        self.play(
            UpdateFromFunc(phi_char, lambda m: m.look_at(exinformula_2)),
            run_time=1
        )
        self.play(
            UpdateFromFunc(phi_char, lambda m: m.look_back()),
            run_time=1
        )
        self.play(
            UpdateFromFunc(phi_char2, lambda m: m.look_at(exinformula_2)),
            run_time=1
        )
        self.play(
            UpdateFromFunc(phi_char2, lambda m: m.look_back()),
            run_time=1
        )
        self.play(FadeOut(A_circle_exin2, shift=UP), FadeOut(B_circle_exin2, shift=UP),
                  FadeOut(exinformula_2))
        
        # 3 sets (inclusion exclusion)
        A_text   = MathTex("A", color=MY_GREEN).move_to(ORIGIN + UP*1.125 + LEFT*5)
        B_text   = MathTex("B", color= MY_PINK).move_to(ORIGIN + DOWN*1.125 + LEFT*5)
        C_text   = MathTex("C", color= MY_BLUE ).move_to(ORIGIN + UP*1.125 + RIGHT*2)
        A_circle = Circle(color=MY_GREEN).move_to(ORIGIN + UP*1.125 + LEFT*3)
        B_circle = Circle(color= MY_PINK).move_to(ORIGIN + DOWN*1.125 + LEFT*3)
        C_circle = Circle(color= MY_BLUE).move_to(ORIGIN + UP*1.125 + RIGHT*4)

        self.play(Write(A_text), 
                  Write(B_text), 
                  Write(C_text), 
                  Create(A_circle), 
                  Create(B_circle), 
                  Create(C_circle))
        self.wait(1)
        self.play(FadeOut(A_text, shift=RIGHT), FadeOut(A_circle, shift=RIGHT),
                  FadeOut(B_text, shift=RIGHT), FadeOut(B_circle, shift=RIGHT),
                  FadeOut(C_text, shift=RIGHT), FadeOut(C_circle, shift=RIGHT))
        
        A_circle_exin3 = Circle(color=MY_GREEN).move_to(ORIGIN + LEFT*0.45 + UP)
        B_circle_exin3 = Circle(color= MY_PINK).move_to(ORIGIN + RIGHT*0.45 + UP)
        C_circle_exin3 = Circle(color= MY_BLUE).move_to(ORIGIN)
        exinformula_3  = MathTex(r"|A \cup B \cup C| = |A| + |B| + |C| "
                                r"- (|A \cap B| + |A \cap C| + |B \cap C|) "
                                r"+ |A \cap B \cap C|", 
                                color= MY_YELLOW, ).move_to(ORIGIN + DOWN*1.75)
        exinformula_3.scale(0.7)  

        self.play(Create(A_circle_exin3), 
                  Create(B_circle_exin3), 
                  Create(C_circle_exin3), 
                  Write(exinformula_3))
        self.wait(3)
        self.play(
            UpdateFromFunc(phi_char, lambda m: m.look_at(exinformula_3)),
            run_time=1
        )
        self.play(
            UpdateFromFunc(phi_char, lambda m: m.look_back()),
            run_time=1
        )
        self.play(
            UpdateFromFunc(phi_char2, lambda m: m.look_at(exinformula_3)),
            run_time=1
        )
        self.play(
            UpdateFromFunc(phi_char2, lambda m: m.look_back()),
            run_time=1
        )
        self.play(FadeOut(A_circle_exin3, shift=LEFT), 
                  FadeOut(B_circle_exin3, shift=RIGHT),
                  FadeOut(C_circle_exin3, shift=DOWN),
                  FadeOut(exinformula_3))

        exin_general = MathTex(
                        r"\left|\bigcup_{i=1}^{n} A_i\right|"
                        r"= \sum_{i=1}^{n} |A_i|"
                        r" - \sum_{1 \le i < j \le n} |A_i \cap A_j|"
                        r" + \sum_{1 \le i < j < k \le n} |A_i \cap A_j \cap A_k|"
                        r" - \sum_{1 \le i < j < k < \ell \le n} |A_i \cap A_j \cap A_k \cap A_\ell|"
                        r" + \cdots"
                        r" + (-1)^{n+1} |A_1 \cap A_2 \cap \cdots \cap A_n|",
                        color=MY_YELLOW
                    ).scale(0.45)
        
        self.play(Write(exin_general))
        self.wait(3)
        self.play(
            UpdateFromFunc(phi_char, lambda m: m.look_at(exinformula_3)),
            run_time=1
        )
        self.play(
            UpdateFromFunc(phi_char, lambda m: m.look_back()),
            run_time=1
        )
        self.play(
            UpdateFromFunc(phi_char2, lambda m: m.look_at(exinformula_3)),
            run_time=1
        )
        self.play(
            UpdateFromFunc(phi_char2, lambda m: m.look_back()),
            run_time=1
        )
        self.play(FadeOut(exin_general))

        exin_compact = MathTex(
                        r"\left|\bigcup_{i=1}^{n} A_i\right|"
                        r"= \sum_{k=1}^{n} (-1)^{k+1}"
                        r"\!\!\!\sum_{1 \le i_1 < \cdots < i_k \le n}"
                        r"\left|A_{i_1} \cap \cdots \cap A_{i_k}\right|",
                        color=MY_YELLOW
                    ).scale(0.7)
        
        self.play(Write(exin_compact))
        self.wait(3)
        self.play(
            UpdateFromFunc(phi_char, lambda m: m.look_at(exinformula_3)),
            run_time=1
        )
        self.play(
            UpdateFromFunc(phi_char, lambda m: m.look_back()),
            run_time=1
        )
        self.play(
            UpdateFromFunc(phi_char2, lambda m: m.look_at(exinformula_3)),
            run_time=1
        )
        self.play(
            UpdateFromFunc(phi_char2, lambda m: m.look_back()),
            run_time=1
        )
        self.play(FadeOut(exin_compact))

        M_def = MathTex(
                    r"M = \{1,2,\ldots,n\}",
                    color=MY_YELLOW
                ).move_to(ORIGIN + UP*1.125)
        phi_def = MathTex(
                    r"\varphi(n)",
                    color=MY_YELLOW
                )
        phi_example = MathTex(
                        r"\varphi(4) = 2",
                        color=MY_YELLOW
                    ).move_to(ORIGIN + DOWN*1.125)
        
        self.play(Write(M_def))
        self.wait(2)
        self.play(Write(phi_def))
        self.wait(2)
        self.play(Write(phi_example))
        self.wait(3)
        self.play(
            UpdateFromFunc(phi_char, lambda m: m.look_at(exinformula_3)),
            run_time=1
        )
        self.play(
            UpdateFromFunc(phi_char, lambda m: m.look_back()),
            run_time=1
        )
        self.play(
            UpdateFromFunc(phi_char2, lambda m: m.look_at(exinformula_3)),
            run_time=1
        )
        self.play(
            UpdateFromFunc(phi_char2, lambda m: m.look_back()),
            run_time=1
        )
        self.play(FadeOut(M_def, shift=LEFT), 
                  FadeOut(phi_def, shift=RIGHT),
                  FadeOut(phi_example, shift=DOWN)
        )

        n_factor = MathTex(
            r"n = p_1^{a_1} p_2^{a_2} \cdots p_k^{a_k}",
            color=MY_YELLOW
        ).move_to(ORIGIN + UP*1.125)
        phi_union = MathTex(
            r"\varphi(n) = n - \left|\bigcup_{i=1}^{k} A_i\right|",
            color=MY_YELLOW
        )
        self.play(Write(n_factor))
        self.wait(2)
        self.play(Write(phi_union))
        self.wait(2)
        self.wait(3)
        self.play(
            UpdateFromFunc(phi_char, lambda m: m.look_at(exinformula_3)),
            run_time=1
        )
        self.play(
            UpdateFromFunc(phi_char, lambda m: m.look_back()),
            run_time=1
        )
        self.play(
            UpdateFromFunc(phi_char2, lambda m: m.look_at(exinformula_3)),
            run_time=1
        )
        self.play(
            UpdateFromFunc(phi_char2, lambda m: m.look_back()),
            run_time=1
        )
        self.play(FadeOut(n_factor, shift=LEFT), 
                  FadeOut(phi_union, shift=RIGHT),
        )

        phi_expanded = MathTex(
            r"\varphi(n) = n - \Bigg["
            r"\sum_{i=1}^{k} |A_i|"
            r" - \sum_{1 \le i < j \le k} |A_i \cap A_j|"
            r" + \sum_{1 \le i < j < \ell \le k} |A_i \cap A_j \cap A_\ell|"
            r" - \cdots"
            r" + (-1)^{k+1} |A_1 \cap \cdots \cap A_k|"
            r"\Bigg]",
            color=MY_YELLOW
        ).scale(0.55)
        self.play(Write(phi_expanded))
        self.wait(3)
        self.play(
            UpdateFromFunc(phi_char, lambda m: m.look_at(exinformula_3)),
            run_time=1
        )
        self.play(
            UpdateFromFunc(phi_char, lambda m: m.look_back()),
            run_time=1
        )
        self.play(
            UpdateFromFunc(phi_char2, lambda m: m.look_at(exinformula_3)),
            run_time=1
        )
        self.play(
            UpdateFromFunc(phi_char2, lambda m: m.look_back()),
            run_time=1
        )
        self.play(FadeOut(phi_expanded, shift=LEFT), 
        )

        phi_proof = MathTex(
            r"|A_i|=\frac{n}{p_i},\quad"
            r"|A_i\cap A_j|=\frac{n}{p_i p_j},\quad"
            r"|A_i\cap A_j\cap A_\ell|=\frac{n}{p_i p_j p_\ell}",
            color=MY_YELLOW
        ).scale(0.9)
        self.play(Write(phi_proof))
        self.wait(3)
        self.play(
            UpdateFromFunc(phi_char, lambda m: m.look_at(exinformula_3)),
            run_time=1
        )
        self.play(
            UpdateFromFunc(phi_char, lambda m: m.look_back()),
            run_time=1
        )
        self.play(
            UpdateFromFunc(phi_char2, lambda m: m.look_at(exinformula_3)),
            run_time=1
        )
        self.play(
            UpdateFromFunc(phi_char2, lambda m: m.look_back()),
            run_time=1
        )
        self.play(FadeOut(phi_proof, shift=RIGHT), 
        )

        phi_subs = MathTex(
            r"\varphi(n)="
            r"n\Bigg["
            r"1-\sum\frac{1}{p_i}"
            r"+\sum\frac{1}{p_i p_j}"
            r"-\sum\frac{1}{p_i p_j p_\ell}"
            r"+\cdots"
            r"+(-1)^k\frac{1}{p_1\cdots p_k}"
            r"\Bigg]",
            color=MY_YELLOW
        ).scale(0.75)
        self.play(Write(phi_subs))
        self.wait(3)
        self.play(
            UpdateFromFunc(phi_char, lambda m: m.look_at(exinformula_3)),
            run_time=1
        )
        self.play(
            UpdateFromFunc(phi_char, lambda m: m.look_back()),
            run_time=1
        )
        self.play(
            UpdateFromFunc(phi_char2, lambda m: m.look_at(exinformula_3)),
            run_time=1
        )
        self.play(
            UpdateFromFunc(phi_char2, lambda m: m.look_back()),
            run_time=1
        )
        self.play(FadeOut(phi_subs)
        )

        phi_final = MathTex(
            r"\varphi(n)=n\prod_{i=1}^{k}\left(1-\frac{1}{p_i}\right)",
            color=MY_YELLOW
        )
        self.play(Write(phi_final))
        self.wait(3)
        self.play(
            UpdateFromFunc(phi_char, lambda m: m.look_at(exinformula_3)),
            run_time=1
        )
        self.play(
            UpdateFromFunc(phi_char, lambda m: m.look_back()),
            run_time=1
        )
        self.play(
            UpdateFromFunc(phi_char2, lambda m: m.look_at(exinformula_3)),
            run_time=1
        )
        self.play(
            UpdateFromFunc(phi_char2, lambda m: m.look_back()),
            run_time=1
        )
        self.play(FadeOut(phi_final)
        )

        phi_example = MathTex(
            r"\varphi(4) = 4 \left( 1 - \frac{1}{2} \right) = 2"
        )
        self.play(Write(phi_example))
        self.wait(2)
        self.play(
            UpdateFromFunc(phi_char, lambda m: m.look_at(exinformula_3)),
            run_time=1
        )
        self.play(
            UpdateFromFunc(phi_char, lambda m: m.look_back()),
            run_time=1
        )
        self.play(
            UpdateFromFunc(phi_char2, lambda m: m.look_at(exinformula_3)),
            run_time=1
        )
        self.play(
            UpdateFromFunc(phi_char2, lambda m: m.look_back()),
            run_time=1
        )
        self.play(FadeOut(phi_example)
        )

        ending = Text(
            "Thanks For Listening",
            font_size=48,
            weight=BOLD,
            color= MY_PINK,
            slant=ITALIC
        )
        self.play(
            FadeIn(ending, shift=UP),
            run_time=1.5
        )
        self.wait(1)
        self.play(FadeOut(ending))
        self.wait(1)



        




    