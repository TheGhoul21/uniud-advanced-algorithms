#!/usr/bin/env python3
"""
Z-Algorithm Manim Animation
Render with: manim -pql z_algorithm.py ZAlgorithmScene
(use -pqh for high quality)
"""

from manim import *

# ─── Palette ────────────────────────────────────────────────────────────────
C_BG        = "#1e1e2e"
C_TEXT      = "#cdd6f4"
C_ACCENT    = "#89b4fa"   # blue  – current index i
C_MATCH     = "#a6e3a1"   # green – matched characters
C_MISMATCH  = "#f38ba8"   # red   – mismatch
C_ZBOX      = "#fab387"   # orange – Z-box [L, R]
C_PREFIX    = "#cba6f7"   # purple – prefix highlight
C_SEPARATOR = "#f9e2af"   # yellow – $ separator
C_SUBTITLE  = "#6c7086"

CELL_W = 0.55
CELL_H = 0.55

# ─── Helpers ────────────────────────────────────────────────────────────────

def make_string_cells(s, font_size=22, cell_w=CELL_W, cell_h=CELL_H):
    """Return (VGroup of squares, VGroup of char labels, VGroup of index labels)."""
    cells  = VGroup()
    chars  = VGroup()
    idxs   = VGroup()
    for k, ch in enumerate(s):
        sq = Square(side_length=cell_w, stroke_color=C_TEXT, stroke_width=1.5,
                    fill_color=C_BG, fill_opacity=1)
        sq.move_to(RIGHT * k * cell_w)
        color = C_SEPARATOR if ch == "$" else C_TEXT
        lbl = Text(ch, font_size=font_size, color=color).move_to(sq.get_center())
        idx = Text(str(k), font_size=13, color=C_SUBTITLE).next_to(sq, DOWN, buff=0.08)
        cells.add(sq)
        chars.add(lbl)
        idxs.add(idx)
    return cells, chars, idxs


def make_z_cells(z_arr, font_size=20, cell_w=CELL_W, cell_h=CELL_H):
    """Return (VGroup of squares, VGroup of value labels)."""
    cells = VGroup()
    vals  = VGroup()
    for k, v in enumerate(z_arr):
        sq = Square(side_length=cell_w, stroke_color=C_TEXT, stroke_width=1.5,
                    fill_color=C_BG, fill_opacity=1)
        sq.move_to(RIGHT * k * cell_w)
        txt = "–" if v == -1 else str(v)
        lbl = Text(txt, font_size=font_size, color=C_ACCENT).move_to(sq.get_center())
        cells.add(sq)
        vals.add(lbl)
    return cells, vals


def compute_z(s):
    n = len(s)
    Z = [0] * n
    Z[0] = n
    L = R = 0
    for i in range(1, n):
        if i <= R:
            Z[i] = min(R - i + 1, Z[i - L])
        while i + Z[i] < n and s[Z[i]] == s[i + Z[i]]:
            Z[i] += 1
        if i + Z[i] - 1 > R:
            L, R = i, i + Z[i] - 1
    return Z


# ═══════════════════════════════════════════════════════════════════════════
class ZAlgorithmScene(Scene):
# ═══════════════════════════════════════════════════════════════════════════

    def construct(self):
        self.camera.background_color = C_BG
        self._part1_intro()
        self._part2_intuition()
        self._part3_pattern_matching()

    # ── Part 0: Title ────────────────────────────────────────────────────

    def _part1_intro(self):
        title = Text("Z-Algorithm", font_size=52, color=C_ACCENT, weight=BOLD)
        sub   = Text("Linear-time string analysis  ·  O(n)", font_size=24, color=C_SUBTITLE)
        sub.next_to(title, DOWN, buff=0.3)
        desc = Text(
            "Z[i]  =  length of the longest substring\nstarting at i that matches a prefix of s",
            font_size=21, color=C_TEXT, line_spacing=1.4
        )
        desc.next_to(sub, DOWN, buff=0.5)
        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(sub), run_time=0.8)
        self.play(FadeIn(desc), run_time=1)
        self.wait(2)
        self.play(FadeOut(VGroup(title, sub, desc)))

    # ── Part 1: Intuition on "abacaba" ────────────────────────────────────

    def _part2_intuition(self):
        s = "abacaba"
        n = len(s)
        Z = compute_z(s)   # [7,0,1,0,3,0,1]

        # ── Header
        header = Text("Intuizione  ·  s = \"abacaba\"", font_size=30, color=C_ACCENT)
        header.to_edge(UP, buff=0.35)
        self.play(Write(header))
        
        # ── Variables Box (L, R)
        l_text = VGroup(Text("L =", font_size=22, color=C_ZBOX), Integer(0, font_size=22, color=C_ZBOX)).arrange(RIGHT, buff=0.2)
        r_text = VGroup(Text("R =", font_size=22, color=C_ZBOX), Integer(0, font_size=22, color=C_ZBOX)).arrange(RIGHT, buff=0.2)
        lr_box = VGroup(l_text, r_text).arrange(RIGHT, buff=0.6)
        lr_box.to_corner(UR, buff=0.35)
        self.play(FadeIn(lr_box))

        # ── Code Block
        code_str = [
            "if i > R:",                       # 0
            "    match naive",                 # 1
            "else:",                           # 2
            "    k = i - L",                   # 3
            "    rem = R - i + 1",             # 4
            "    if Z[k] < rem:",              # 5
            "        Z[i] = Z[k]",             # 6
            "    else:",                       # 7
            "        match da R"               # 8
        ]
        
        code_lines = VGroup()
        for line in code_str:
            t = Text(line.strip(), font_size=15, color=C_TEXT)
            code_lines.add(t)
        code_lines.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        
        # apply indentation
        for i, line in enumerate(code_str):
            indent = len(line) - len(line.lstrip())
            if indent > 0:
                code_lines[i].shift(RIGHT * indent * 0.08)

        code_lines.to_corner(UL, buff=0.35)
        code_lines.shift(DOWN * 0.6 + RIGHT * 0.2)
        
        code_bg = RoundedRectangle(corner_radius=0.1, color=C_SUBTITLE, stroke_width=1, fill_color="#11111b", fill_opacity=0.8)
        code_bg.surround(code_lines, buff=0.2)
        code_group = VGroup(code_bg, code_lines)
        self.play(FadeIn(code_group))

        active_line_rect = None
        def highlight_code(line_indices):
            nonlocal active_line_rect
            target_lines = VGroup(*[code_lines[idx] for idx in line_indices])
            new_rect = SurroundingRectangle(target_lines, color=C_PREFIX, fill_color=C_PREFIX, fill_opacity=0.25, stroke_width=0, buff=0.06)
            if active_line_rect:
                return ReplacementTransform(active_line_rect, new_rect)
            else:
                active_line_rect = new_rect
                return FadeIn(new_rect)

        # ── String row
        cells, chars, idxs = make_string_cells(s)
        str_group = VGroup(cells, chars, idxs).move_to(ORIGIN + UP * 1.0)
        # Shift string to the right slightly to leave room for code block
        str_group.shift(RIGHT * 1.5)
        self.play(FadeIn(str_group))

        # ── Z-array row
        z_init = [-1] * n
        z_cells, z_vals = make_z_cells(z_init)
        z_group = VGroup(z_cells, z_vals).move_to(ORIGIN + DOWN * 0.2)
        z_group.align_to(str_group, LEFT)
        z_label = Text("Z[ ]", font_size=20, color=C_ACCENT).next_to(z_group, LEFT, buff=0.2)
        self.play(FadeIn(z_group), FadeIn(z_label))

        # Pointers for L and R
        def make_pointer(txt_str, color):
            t = Text(txt_str, font_size=16, color=color)
            tri = Triangle(fill_opacity=1, color=color).scale(0.12).rotate(PI)
            grp = VGroup(t, tri).arrange(DOWN, buff=0.08)
            return grp

        l_ptr = make_pointer("L", C_ZBOX)
        r_ptr = make_pointer("R", C_ZBOX)
        
        persistent_zbox = None

        # ── Explanation text box (bottom)
        expl_box = Rectangle(width=11, height=1.1, fill_color="#11111b",
                              fill_opacity=0.9, stroke_color=C_SUBTITLE, stroke_width=1)
        expl_box.to_edge(DOWN, buff=0.2)
        self.play(FadeIn(expl_box))

        current_expl = None
        def show_expl(text_str, color=C_TEXT):
            nonlocal current_expl
            t = Text(text_str, font_size=19, color=color).move_to(expl_box.get_center())
            if current_expl:
                self.play(FadeOut(current_expl), FadeIn(t), run_time=0.6)
            else:
                self.play(FadeIn(t), run_time=0.6)
            current_expl = t
            return current_expl

        # Z[0] = n by definition
        self.play(cells[0].animate.set_fill(C_PREFIX, opacity=0.4), run_time=0.8)
        show_expl("Z[0] = n = 7  (per definizione, l'intera stringa)")
        new_val = Text(str(Z[0]), font_size=20, color=C_MATCH).move_to(z_cells[0].get_center())
        self.play(Transform(z_vals[0], new_val), run_time=0.8)
        self.wait(1.5)
        self.play(cells[0].animate.set_fill(C_BG, opacity=1), run_time=0.5)

        L, R = 0, 0

        for i in range(1, n):
            # Highlight current index
            i_lbl = Text("i", font_size=18, color=C_ACCENT).next_to(cells[i], DOWN, buff=0.35)
            self.play(
                cells[i].animate.set_fill(C_ACCENT, opacity=0.35),
                FadeIn(i_lbl, shift=UP*0.15),
                run_time=0.6
            )
            self.wait(0.5)

            k = 0
            # Step by step logic
            if i > R:
                self.play(highlight_code([0, 1]), run_time=0.5)
                show_expl(f"i={i} > R={R}: Fuori dalla Z-box, calcolo manuale (naive)", C_TEXT)
                self.wait(1.5)
                # Naive matching animation
                while i + k < n and s[k] == s[i + k]:
                    self.play(
                        cells[k].animate.set_fill(C_PREFIX, opacity=0.4),
                        cells[i + k].animate.set_fill(C_MATCH, opacity=0.5),
                        run_time=0.6
                    )
                    self.wait(0.5)
                    k += 1
                if i + k < n:
                    self.play(
                        cells[k].animate.set_fill(C_MISMATCH, opacity=0.4),
                        cells[i + k].animate.set_fill(C_MISMATCH, opacity=0.5),
                        run_time=0.6
                    )
                    show_expl(f"Mismatch a indice {i+k}. Z[{i}] = {k}", C_MISMATCH)
                    self.wait(1.5)
                else:
                    show_expl(f"Fine stringa raggiunta. Z[{i}] = {k}", C_MATCH)
                    self.wait(1.5)
            else:
                self.play(highlight_code([2, 3, 4]), run_time=0.5)
                k_idx = i - L
                rem = R - i + 1
                show_expl(f"i={i} <= R={R}: Dentro Z-box. Guardo Z[i-L] = Z[{k_idx}] = {Z[k_idx]}", C_ZBOX)
                self.wait(0.5)
                
                conn_arrow = CurvedArrow(z_cells[i].get_bottom() + DOWN*0.1, z_cells[k_idx].get_bottom() + DOWN*0.1, angle=PI/3, color=C_ZBOX)
                self.play(Create(conn_arrow), z_cells[k_idx].animate.set_fill(C_PREFIX, opacity=0.6), run_time=0.8)
                self.wait(1.5)
                
                if Z[k_idx] < rem:
                    self.play(highlight_code([5, 6]), run_time=0.5)
                    show_expl(f"Z[{k_idx}]={Z[k_idx]} < {rem} (spazio residuo). Z[{i}] = {Z[k_idx]} (copia veloce!)", C_MATCH)
                    self.wait(2.0)
                    k = Z[k_idx]
                    if k > 0:
                        anims = []
                        for m in range(k):
                            anims.append(cells[m].animate.set_fill(C_PREFIX, opacity=0.4))
                            anims.append(cells[i + m].animate.set_fill(C_MATCH, opacity=0.5))
                        self.play(*anims, run_time=0.8)
                        self.wait(1.5)
                else:
                    self.play(highlight_code([7, 8]), run_time=0.5)
                    show_expl(f"Z[{k_idx}]={Z[k_idx]} >= {rem} (residuo). Controllo oltre R={R}!", C_ACCENT)
                    self.wait(2.0)
                    k = rem
                    if k > 0:
                        anims = []
                        for m in range(k):
                            anims.append(cells[m].animate.set_fill(C_PREFIX, opacity=0.4))
                            anims.append(cells[i + m].animate.set_fill(C_MATCH, opacity=0.5))
                        self.play(*anims, run_time=0.8)
                        self.wait(1.0)
                    
                    while i + k < n and s[k] == s[i + k]:
                        self.play(
                            cells[k].animate.set_fill(C_PREFIX, opacity=0.4),
                            cells[i + k].animate.set_fill(C_MATCH, opacity=0.5),
                            run_time=0.6
                        )
                        self.wait(0.5)
                        k += 1
                    if i + k < n:
                        self.play(
                            cells[k].animate.set_fill(C_MISMATCH, opacity=0.4),
                            cells[i + k].animate.set_fill(C_MISMATCH, opacity=0.5),
                            run_time=0.6
                        )
                        show_expl(f"Mismatch a indice {i+k}. Z[{i}] = {k}", C_MISMATCH)
                        self.wait(1.5)
                    else:
                        show_expl(f"Fine stringa raggiunta. Z[{i}] = {k}", C_MATCH)
                        self.wait(1.5)
                
                self.play(FadeOut(conn_arrow), z_cells[k_idx].animate.set_fill(C_BG, opacity=1), run_time=0.5)

            # Update Z cell
            new_val = Text(str(k), font_size=20,
                           color=C_MATCH if k > 0 else C_TEXT).move_to(z_cells[i].get_center())
            self.play(Transform(z_vals[i], new_val), run_time=0.6)
            self.wait(1.0)

            # Update L, R
            if k > 0 and i + k - 1 > R:
                new_L, new_R = i, i + k - 1
                show_expl(f"Nuovo match supera R. Aggiorno Z-box: L={new_L}, R={new_R}", C_ZBOX)
                self.wait(0.5)
                
                anims = [
                    lr_box[0][1].animate.set_value(new_L),
                    lr_box[1][1].animate.set_value(new_R)
                ]
                
                if new_L == new_R:
                    l_target = cells[new_L].get_top() + UP*0.1 + LEFT*0.15
                    r_target = cells[new_R].get_top() + UP*0.1 + RIGHT*0.15
                else:
                    l_target = cells[new_L].get_top() + UP*0.1
                    r_target = cells[new_R].get_top() + UP*0.1
                
                if L == 0 and R == 0:
                    l_ptr.move_to(l_target, aligned_edge=DOWN)
                    r_ptr.move_to(r_target, aligned_edge=DOWN)
                    anims.extend([FadeIn(l_ptr, shift=DOWN*0.2), FadeIn(r_ptr, shift=DOWN*0.2)])
                else:
                    anims.extend([
                        l_ptr.animate.move_to(l_target, aligned_edge=DOWN),
                        r_ptr.animate.move_to(r_target, aligned_edge=DOWN)
                    ])
                
                new_zbox = DashedVMobject(SurroundingRectangle(VGroup(cells[new_L], cells[new_R]), color=C_ZBOX, stroke_width=2, buff=0.06), num_dashes=20)
                if persistent_zbox:
                    anims.append(ReplacementTransform(persistent_zbox, new_zbox))
                else:
                    anims.append(Create(new_zbox))
                persistent_zbox = new_zbox
                
                self.play(*anims, run_time=1.0)
                self.wait(2.0)
                L, R = new_L, new_R

            # Cleanup
            cleanup = [cells[j].animate.set_fill(C_BG, opacity=1) for j in range(n)]
            cleanup.append(FadeOut(i_lbl))
            if active_line_rect:
                cleanup.append(FadeOut(active_line_rect))
                active_line_rect = None
            self.play(*cleanup, run_time=0.6)

        # Final Z-array display
        if current_expl:
            self.play(FadeOut(current_expl), run_time=0.5)
        
        final_e = Text("Z-array completo:  [7, 0, 1, 0, 3, 0, 1]", font_size=19, color=C_ACCENT).move_to(expl_box.get_center())
        self.play(FadeIn(final_e), run_time=0.8)
        self.wait(2.5)
        
        fade_group = VGroup(header, lr_box, str_group, z_group, z_label, expl_box, final_e, code_group)
        if persistent_zbox:
            fade_group.add(persistent_zbox, l_ptr, r_ptr)
        self.play(FadeOut(fade_group))

    # ── Part 2: Pattern Matching con separatore $ ─────────────────────────

    def _part3_pattern_matching(self):
        pattern = "ana"
        text    = "banana"
        sep     = "$"
        s       = pattern + sep + text   # "ana$banana"
        n       = len(s)
        Z       = compute_z(s)
        pat_len = len(pattern)

        # Header
        header = Text("Pattern Matching  ·  P + \"$\" + T", font_size=28, color=C_ACCENT)
        header.to_edge(UP, buff=0.35)
        self.play(Write(header))

        # Show the concatenation step
        p_txt = Text(f'P = "{pattern}"', font_size=26, color=C_PREFIX)
        t_txt = Text(f'T = "{text}"',    font_size=26, color=C_MATCH)
        arrow = Text("→", font_size=26, color=C_TEXT)
        concat_txt = Text(f'S = "{s}"', font_size=26, color=C_TEXT)
        concat_txt[3 + 1 + len(pattern)].set_color(C_SEPARATOR)  # $ char

        info_grp = VGroup(p_txt, t_txt, arrow, concat_txt).arrange(RIGHT, buff=0.4)
        info_grp.next_to(header, DOWN, buff=0.35)
        self.play(FadeIn(info_grp), run_time=1.5)
        self.wait(2.0)

        rule_txt = Text(
            "Regola: se Z[i] = |P|  →  pattern trovato in T alla posizione  i − |P| − 1",
            font_size=18, color=C_TEXT
        )
        rule_txt.next_to(info_grp, DOWN, buff=0.25)
        self.play(FadeIn(rule_txt), run_time=1.0)
        self.wait(2.5)
        self.play(FadeOut(info_grp), FadeOut(rule_txt), run_time=0.8)

        # String cells
        cells, chars, idxs = make_string_cells(s, font_size=21)
        str_grp = VGroup(cells, chars, idxs)
        str_grp.move_to(ORIGIN + UP * 1.5)
        str_grp.shift(LEFT * (n - 1) * CELL_W / 2)
        self.play(FadeIn(str_grp), run_time=1.0)

        # Colour-code separator
        cells[pat_len].set_fill(C_SEPARATOR, opacity=0.25)

        # Bracket labels: Pattern | $ | Text
        pat_brace  = BraceBetweenPoints(
            cells[0].get_bottom(), cells[pat_len - 1].get_bottom(), direction=DOWN
        )
        pat_brace_lbl = pat_brace.get_text("Pattern").set_color(C_PREFIX)
        txt_brace = BraceBetweenPoints(
            cells[pat_len + 1].get_bottom(), cells[-1].get_bottom(), direction=DOWN
        )
        txt_brace_lbl = txt_brace.get_text("Text").set_color(C_MATCH)
        self.play(Create(pat_brace), FadeIn(pat_brace_lbl),
                  Create(txt_brace), FadeIn(txt_brace_lbl), run_time=1.2)
        self.wait(1.5)

        # Z-array row
        z_cells, z_vals = make_z_cells([-1] * n)
        z_grp = VGroup(z_cells, z_vals)
        z_grp.next_to(str_grp, DOWN, buff=0.6)
        z_grp.align_to(str_grp, LEFT)
        z_label = Text("Z[ ]", font_size=20, color=C_ACCENT).next_to(z_grp, LEFT, buff=0.2)
        self.play(FadeIn(z_grp), FadeIn(z_label), run_time=1.0)

        # Explanation box
        expl_box = Rectangle(width=11, height=1.0, fill_color="#11111b",
                              fill_opacity=0.9, stroke_color=C_SUBTITLE, stroke_width=1)
        expl_box.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(expl_box), run_time=0.8)

        current_expl = None
        def show_expl(text_str, color=C_TEXT):
            nonlocal current_expl
            t = Text(text_str, font_size=18, color=color).move_to(expl_box.get_center())
            if current_expl:
                self.play(FadeOut(current_expl), FadeIn(t), run_time=0.6)
            else:
                self.play(FadeIn(t), run_time=0.6)
            current_expl = t
            return current_expl

        matches = []
        L = R = 0

        for i in range(n):
            # Z[0] special
            if i == 0:
                self.play(cells[0].animate.set_fill(C_PREFIX, opacity=0.35), run_time=0.6)
                show_expl("Z[0] = n (definizione, non usato per il matching)")
                new_v = Text(str(n), font_size=20, color=C_TEXT).move_to(z_cells[0].get_center())
                self.play(Transform(z_vals[0], new_v), run_time=0.6)
                self.wait(1.5)
                self.play(cells[0].animate.set_fill(C_BG, opacity=1), run_time=0.5)
                continue

            k = Z[i]
            self.play(cells[i].animate.set_fill(C_ACCENT, opacity=0.35), run_time=0.6)

            # Highlight Z-box
            zbox_rect = zbox_lbl_obj = None
            if i <= R and L < R:
                zbox_rect = SurroundingRectangle(VGroup(cells[L], cells[R]),
                                                  color=C_ZBOX, stroke_width=2, buff=0.03)
                zbox_lbl_obj = Text(f"[{L},{R}]", font_size=14, color=C_ZBOX)
                zbox_lbl_obj.next_to(zbox_rect, UP, buff=0.08)
                self.play(Create(zbox_rect), FadeIn(zbox_lbl_obj), run_time=0.8)
                self.wait(0.5)

            # Highlight matched range
            match_anims = []
            for m in range(k):
                match_anims.append(cells[m].animate.set_fill(C_PREFIX, opacity=0.3))
                if i + m < n:
                    match_anims.append(cells[i + m].animate.set_fill(C_MATCH, opacity=0.4))
            if match_anims:
                self.play(*match_anims, run_time=0.8)
                self.wait(0.5)

            # Check match
            is_match = (k == pat_len and i > pat_len)
            if is_match:
                pos_in_text = i - pat_len - 1
                matches.append(pos_in_text)
                show_expl(f"Z[{i}] = {k} = |P|  ✓  Pattern trovato in T a posizione {pos_in_text}!", C_MATCH)
                self.wait(1.0)
                # Highlight match in text portion
                for m in range(pat_len):
                    self.play(cells[i + m].animate.set_fill(C_MATCH, opacity=0.6), run_time=0.2)
                self.wait(1.0)
            elif k > 0:
                show_expl(f"Z[{i}] = {k}  (match parziale, < |P| = {pat_len})", C_TEXT)
                self.wait(1.0)
            else:
                show_expl(f"Z[{i}] = 0  (nessun match col prefisso)", C_TEXT)
                self.wait(1.0)

            new_v = Text(str(k), font_size=20,
                         color=C_MATCH if is_match else (C_ACCENT if k > 0 else C_TEXT)
                         ).move_to(z_cells[i].get_center())
            self.play(Transform(z_vals[i], new_v), run_time=0.6)
            self.wait(1.5 if is_match else 1.0)

            # Update L, R
            if k > 0 and i + k - 1 > R:
                L, R = i, i + k - 1

            # Cleanup
            cleanup = [cells[j].animate.set_fill(C_BG, opacity=1) for j in range(n) if j != pat_len]
            cleanup.append(cells[pat_len].animate.set_fill(C_SEPARATOR, opacity=0.25))
            if zbox_rect:
                cleanup += [FadeOut(zbox_rect), FadeOut(zbox_lbl_obj)]
            self.play(*cleanup, run_time=0.6)

        # Final result
        if current_expl:
            self.play(FadeOut(current_expl), run_time=0.5)
            
        match_str = ", ".join(str(m) for m in matches)
        result_txt = Text(
            f"Pattern \"{pattern}\" trovato in \"{text}\" alle posizioni: {match_str}",
            font_size=22, color=C_MATCH
        )
        result_txt.to_edge(DOWN, buff=0.3)
        self.play(FadeOut(expl_box), run_time=0.6)
        self.play(Write(result_txt), run_time=1.0)
        self.wait(3.5)
        self.play(FadeOut(VGroup(header, str_grp, z_grp, z_label, z_label,
                                  pat_brace, pat_brace_lbl, txt_brace, txt_brace_lbl,
                                  result_txt)), run_time=1.0)

        # Complexity outro
        outro = VGroup(
            Text("Complessità:", font_size=26, color=C_ACCENT),
            Text("Tempo: O(n)  –  ogni carattere viene confrontato al più 2 volte",
                 font_size=22, color=C_TEXT),
            Text("Spazio: O(n)  –  per l'array Z",
                 font_size=22, color=C_TEXT),
        ).arrange(DOWN, buff=0.3).move_to(ORIGIN)
        self.play(FadeIn(outro))
        self.wait(3)
        self.play(FadeOut(outro))
