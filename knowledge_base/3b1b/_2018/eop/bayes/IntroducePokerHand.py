# Source: 3b1b/_2018/eop/bayes.py
# Description: [3b1b translated] 展示撲克牌局中，玩家根據公共牌和對手行為，使用貝氏定理更新對手持有同花牌型機率的視覺化過程。


from manim import *
import itertools

class IntroducePokerHand(Scene):
    def __init__(
        self,
        community_cards_center=1.5*DOWN,
        community_card_values=["10S", "QH", "AH", "2C", "5H"],
        your_hand_values=["JS", "KC"],
        **kwargs
    ):
        super().__init__(**kwargs)
        self.community_cards_center = community_cards_center
        self.community_card_values = community_card_values
        self.your_hand_values = your_hand_values

    def construct(self):
        self.add_cards()
        self.indicate_straight()
        self.show_flush_potential()
        self.compute_flush_probability()
        self.show_flush_sample_space()
        self.talk_through_sample_space()
        self.place_high_bet()
        self.change_belief()
        self.move_community_cards_out_of_the_way()
        self.name_bayes_rule()

    def add_cards(self):
        you, her = self.you, self.her
        community_cards = VGroup(*[PlayingCard(value) for value in self.community_card_values])
        community_cards.arrange(RIGHT)
        community_cards.move_to(self.community_cards_center)
        
        deck = VGroup(*[PlayingCard(turned_over=True) for _ in range(5)])
        for i, card in enumerate(deck):
            card.shift(i*(0.03*RIGHT + 0.015*DOWN))
        deck.next_to(community_cards, LEFT)

        you.hand = self.get_hand(you, self.your_hand_values)
        her.hand = self.get_hand(her, None)
        hand_cards = VGroup(*itertools.chain(*list(zip(you.hand, her.hand))))

        self.add(deck)
        for group in [hand_cards, community_cards]:
            for card in group:
                card.generate_target()
                card.scale(0.01)
                card.move_to(deck[-1].get_corner(UP+RIGHT))
            self.play(LaggedStartMap(MoveToTarget, group, lag_ratio=0.8))
            self.wait()
        self.wait()

        self.community_cards = community_cards
        self.deck = deck

    def indicate_straight(self):
        you = self.you
        community_cards = self.community_cards
        you.hand.save_state()
        you.hand.generate_target()
        for card in you.hand.target:
            card.set_height(community_cards.get_height())

        selected_community_cards = VGroup(*[card for card in community_cards if card.numerical_value >= 10])
        selected_community_cards.submobjects.sort(key=lambda c: c.numerical_value)

        selected_community_cards.save_state()
        for card in selected_community_cards:
            card.generate_target()

        straight_cards = VGroup(*itertools.chain(
            you.hand.target, 
            [c.target for c in selected_community_cards]
        ))
        straight_cards.submobjects.sort(key=lambda c: c.numerical_value)
        straight_cards.arrange(RIGHT, buff=SMALL_BUFF)
        straight_cards.next_to(community_cards, UP, aligned_edge=LEFT)
        you.hand.target.shift(MED_SMALL_BUFF*UP)

        self.play(LaggedStartMap(
            MoveToTarget,
            selected_community_cards,
            run_time=1.5
        ))
        self.play(MoveToTarget(you.hand))
        self.play(LaggedStartMap(
            ApplyMethod,
            straight_cards,
            lambda m: (m.set_color, YELLOW),
            rate_func=there_and_back,
            run_time=1.5,
            lag_ratio=0.5,
            remover=True,
        ))
        self.play(you.animate.change("hooray", straight_cards))
        self.wait(2)
        self.play(
            selected_community_cards.animate.restore(),
            you.hand.animate.restore(),
            you.animate.change_mode("happy")
        )
        self.wait()

    def show_flush_potential(self):
        you, her = self.you, self.her
        heart_cards = VGroup(*[c for c in self.community_cards if c.suit == "hearts"])
        heart_cards.save_state()

        her.hand.save_state()
        her.hand.generate_target()
        her.hand.target.arrange(RIGHT)
        her.hand.target.next_to(heart_cards, UP)
        her.hand.target.to_edge(UP)

        her.glasses.save_state()
        her.glasses.move_to(her.hand.target)
        her.glasses.set_fill(opacity=0)

        heart_qs = VGroup()
        hearts = VGroup()
        q_marks = VGroup()
        for target in her.hand.target:
            heart = SuitSymbol("hearts")
            q_mark = MathTex("?")
            heart_q = VGroup(heart, q_mark)
            for mob in heart_q:
                mob.set_height(0.5)
            heart_q.arrange(RIGHT, buff=SMALL_BUFF)
            heart_q.move_to(target)
            heart_qs.add(heart, q_mark)
            hearts.add(heart)
            q_marks.add(q_mark)

        self.play(heart_cards.animate.shift(heart_cards.get_height()*UP))
        self.play(you.animate.change_mode("hesitant"))
        self.play(MoveToTarget(her.hand))
        self.play(LaggedStartMap(DrawBorderThenFill, heart_qs))
        self.play(
            her.animate.change("happy"),
            her.glasses.animate.restore(),
        )
        self.pi_creatures.remove(her)
        new_suit_pairs = [
            ("clubs", "diamonds"),
            ("diamonds", "spades"),
            ("spades", "clubs"),
            ("hearts", "hearts"),
        ]
        for new_suit_pair in new_suit_pairs:
            new_symbols = VGroup(*list(map(SuitSymbol, new_suit_pair)))
            for new_symbol, heart in zip(new_symbols, hearts):
                new_symbol.replace(heart, dim_to_match=1)
            self.play(Transform(
                hearts, new_symbols,
                lag_ratio=0.5
            ))
            self.wait()
        self.play(FadeOut(heart_qs))
        self.play(
            heart_cards.animate.restore(),
            her.hand.animate.restore(),
            you.animate.change_mode("pondering"),
        )

        self.q_marks = q_marks

    def compute_flush_probability(self):
        you, her = self.you, self.her
        equation = MathTex(
            r"{ {10 \choose 2}", r"\over", r"{45 \choose 2} }", 
            r"=", r"{45 \over 990}", r"\approx", r"4.5\%"
        )
        equation.next_to(self.community_cards, UP, buff=LARGE_BUFF)
        percentage = equation[-1]  # 4.5% 部分

        ten = VGroup(*equation[0][1:3])
        num_hearts = Tex(r"\# \text{ Remaining hearts}")
        num_hearts.scale(0.75)
        num_hearts.next_to(ten, UP, aligned_edge=LEFT)
        num_hearts.to_edge(UP)
        num_hearts.set_color(RED)
        num_hearts_arrow = Arrow(
            num_hearts.get_bottom(), ten.get_right(),
            color=RED, buff=SMALL_BUFF
        )

        fourty_five = VGroup(*equation[2][1:3])
        num_cards = Tex(r"\# \text{ Remaining cards}")
        num_cards.scale(0.75)
        num_cards.next_to(fourty_five, LEFT)
        num_cards.to_edge(LEFT)
        num_cards.set_color(BLUE)
        num_cards_arrow = Arrow(
            num_cards, fourty_five,
            color=BLUE, buff=SMALL_BUFF
        )

        self.play(LaggedStartMap(FadeIn, equation))
        self.wait(2)
        self.play(
            FadeIn(num_hearts), 
            Create(num_hearts_arrow),
            ten.animate.set_color(RED),
        )
        self.play(
            FadeIn(num_cards), 
            Create(num_cards_arrow),
            fourty_five.animate.set_color(BLUE)
        )
        self.wait(3)
        equation.remove(percentage)
        self.play(*[FadeOut(mob) for mob in [
            equation, 
            num_hearts, num_hearts_arrow,
            num_cards, num_cards_arrow,
        ]])

        self.percentage = percentage

    def show_flush_sample_space(self):
        you, her = self.you, self.her
        percentage = self.percentage

        # 創建簡單的樣本空間表示（替代原來的 SampleSpaceScene）
        sample_space = Rectangle(height=3, width=5)
        sample_space.set_fill(opacity=0.5)
        sample_space.set_stroke(WHITE, 2)
        sample_space.add_title("Your belief")
        sample_space.move_to(VGroup(you.hand, her.hand))
        sample_space.to_edge(UP, buff=MED_SMALL_BUFF)
        
        # 水平分割
        p = 1./22
        top_part = Rectangle(height=3*p, width=5)
        top_part.set_fill(RED, opacity=0.7)
        top_part.set_stroke(WHITE, 2)
        top_part.move_to(sample_space.get_top(), aligned_edge=UP)
        
        bottom_part = Rectangle(height=3*(1-p), width=5)
        bottom_part.set_fill(BLUE_E, opacity=0.7)
        bottom_part.set_stroke(WHITE, 2)
        bottom_part.next_to(top_part, DOWN, buff=0)
        
        sample_space = VGroup(top_part, bottom_part)
        
        # 添加標籤
        top_label = MathTex("4.5\%").next_to(top_part, LEFT)
        bottom_label = MathTex("95.5\%").next_to(bottom_part, LEFT)
        
        # 添加括號
        top_brace = Brace(top_part, LEFT)
        bottom_brace = Brace(bottom_part, LEFT)

        self.play(FadeIn(sample_space))
        self.play(ReplacementTransform(percentage, top_label))
        self.play(*[GrowFromCenter(brace) for brace in [top_brace, bottom_brace]])
        self.wait(2)
        self.play(Write(bottom_label))
        self.wait(2)

        self.sample_space = sample_space
        self.sample_space.horizontal_parts = VGroup(top_part, bottom_part)
        self.sample_space.horizontal_parts.labels = VGroup(top_label, bottom_label)

    def talk_through_sample_space(self):
        her = self.her
        top_part, bottom_part = self.sample_space.horizontal_parts

        flush_hands, non_flush_hands = hand_lists = [
            [self.get_hand(her, keys) for keys in key_list]
            for key_list in [
                [("3H", "8H"), ("4H", "5H"), ("JH", "KH")],
                [("AC", "6D"), ("3D", "6S"), ("JH", "4C")],
            ]
        ]   
        for hand_list, part in zip(hand_lists, [top_part, bottom_part]):
            self.play(Indicate(part, scale_factor=1))
            for hand in hand_list:
                hand.save_state()
                hand.scale(0.01)
                hand.move_to(part.get_right())
                self.play(hand.animate.restore())
            self.wait()
        self.wait()
        self.play(*[FadeOut(hand) for hand in itertools.chain(*hand_lists)])

    def place_high_bet(self):
        you, her = self.you, self.her
        pre_money = VGroup(*[
            VGroup(*[MathTex(r"\$") for _ in range(10)])
            .arrange(RIGHT, buff=SMALL_BUFF)
            for _ in range(4)
        ]).arrange(UP, buff=SMALL_BUFF)
        money = VGroup(*itertools.chain(*pre_money))
        money.set_color(GREEN)
        money.scale(0.8)
        money.next_to(her.hand, DOWN)
        for dollar in money:
            dollar.save_state()
            dollar.scale(0.01)
            dollar.move_to(her.get_boundary_point(RIGHT))
            dollar.set_fill(opacity=0)

        self.play(LaggedStartMap(
            ApplyMethod,
            money,
            lambda m: (m.restore,),
            run_time=5,
        ))
        self.play(you.animate.change_mode("confused"))
        self.wait()

        self.money = money

    def change_belief(self):
        numbers = self.sample_space.horizontal_parts.labels
        rect = Rectangle(stroke_width=0)
        rect.set_fill(BLACK, 1)
        rect.stretch_to_fit_width(numbers.get_width())
        rect.stretch_to_fit_height(self.sample_space.get_height())
        rect.move_to(numbers, UP)

        self.play(FadeIn(rect))
        # 簡單的動畫替代原來的 division change
        self.play(
            self.sample_space.horizontal_parts[0].animate.stretch(0.2/0.045, 1, about_edge=UP),
            self.sample_space.horizontal_parts[1].animate.stretch(0.8/0.955, 1, about_edge=DOWN),
            rect.animate,
            run_time=3,
            rate_func=there_and_back
        )
        self.play(FadeOut(rect))

    def move_community_cards_out_of_the_way(self):
        cards = self.community_cards
        cards.generate_target()
        cards.target.arrange(
            RIGHT, buff=-cards[0].get_width() + MED_SMALL_BUFF,
        )
        cards.target.move_to(self.deck)
        cards.target.to_edge(LEFT)

        self.play(
            self.deck.animate.scale(0.7),
            self.deck.animate.next_to(cards.target, UP),
            self.deck.animate.to_edge(LEFT),
            self.sample_space.animate.shift(3*DOWN),
            MoveToTarget(cards)
        )

    def name_bayes_rule(self):
        title = TexText("Bayes' rule")
        title.set_color(BLUE)
        title.to_edge(UP)
        subtitle = TexText("Update ", "prior ", "beliefs")
        subtitle.scale(0.8)
        subtitle.next_to(title, DOWN)
        prior_word = subtitle[1]  # "prior" 部分
        numbers = self.sample_space.horizontal_parts.labels
        rect = SurroundingRectangle(numbers, color=GREEN)
        arrow = Arrow(prior_word.get_bottom(), rect.get_top())
        arrow.set_color(GREEN)

        words = TexText(
            r"Maybe she really \\ does have a flush $\dots$",
            alignment=""
        )
        words.scale(0.7)
        words.next_to(self.money, DOWN, aligned_edge=LEFT)

        self.play(
            Write(title, run_time=2),
            self.you.animate.change_mode("pondering")
        )
        self.wait()
        self.play(FadeIn(subtitle))
        self.play(prior_word.animate.set_color(GREEN))
        self.play(
            Create(rect),
            Create(arrow)
        )
        self.wait(3)
        self.play(Write(words))
        self.wait(3)

    def create_pi_creatures(self):
        you = PiCreature(color=BLUE_D)
        her = PiCreature(color=BLUE_B).flip()
        for pi in [you, her]:
            pi.scale(0.5)
        you.to_corner(UL)
        her.to_corner(UR)
        you.make_eye_contact(her)

        glasses = SunGlasses(her)
        her.glasses = glasses

        self.you = you
        self.her = her
        self.pi_creatures = VGroup(you, her)
        self.add(self.pi_creatures)
        return self.pi_creatures

    def get_hand(self, pi_creature, keys=None):
        if keys is not None:
            hand = VGroup(*[PlayingCard(key) for key in keys])
        else:
            hand = VGroup(*[PlayingCard(turned_over=True) for _ in range(2)])
        hand.scale(0.7)
        card1, card2 = hand
        vect = np.sign(pi_creature.get_center()[0])*LEFT
        card2.move_to(card1)
        card2.shift(MED_SMALL_BUFF*RIGHT + SMALL_BUFF*DOWN)
        hand.next_to(
            pi_creature, vect, 
            buff=MED_LARGE_BUFF,
            aligned_edge=UP
        )
        return hand


# 輔助類別定義
class PlayingCard(VGroup):
    def __init__(self, value=None, turned_over=False, **kwargs):
        super().__init__(**kwargs)
        self.value = value
        self.turned_over = turned_over
        
        if turned_over:
            card = Rectangle(height=2, width=1.4, fill_color=BLUE_E, fill_opacity=1, stroke_color=WHITE, stroke_width=2)
            self.add(card)
            self.numerical_value = 0
            self.suit = None
        else:
            card = Rectangle(height=2, width=1.4, fill_color=WHITE, fill_opacity=1, stroke_color=BLACK, stroke_width=2)
            self.add(card)
            # 簡化的牌面表示
            if value:
                rank = value[:-1]
                suit = value[-1]
                self.numerical_value = self.rank_to_value(rank)
                self.suit = self.suit_to_name(suit)
                
                text = Text(f"{rank}\n{suit}", font_size=24)
                text.move_to(card)
                self.add(text)
    
    def rank_to_value(self, rank):
        if rank == "A": return 14
        if rank == "K": return 13
        if rank == "Q": return 12
        if rank == "J": return 11
        return int(rank)
    
    def suit_to_name(self, suit):
        return {"S": "spades", "H": "hearts", "D": "diamonds", "C": "clubs"}[suit]

class SuitSymbol(Circle):
    def __init__(self, suit_name, **kwargs):
        super().__init__(**kwargs)
        self.set_fill(self.suit_color(suit_name), opacity=1)
        self.set_stroke(WHITE, 1)
    
    def suit_color(self, suit_name):
        if suit_name in ["hearts", "diamonds"]:
            return RED
        return BLACK

class SunGlasses(VGroup):
    def __init__(self, pi_creature, **kwargs):
        super().__init__(**kwargs)
        # 簡化的太陽眼鏡表示
        left_lens = Circle(radius=0.15, fill_color=BLACK, fill_opacity=0.7, stroke_color=WHITE)
        right_lens = Circle(radius=0.15, fill_color=BLACK, fill_opacity=0.7, stroke_color=WHITE)
        right_lens.next_to(left_lens, RIGHT, buff=0.1)
        bridge = Rectangle(height=0.05, width=0.1, fill_color=BLACK, fill_opacity=1)
        bridge.move_to(VGroup(left_lens, right_lens))
        
        self.add(left_lens, right_lens, bridge)
        self.move_to(pi_creature.eyes)

class PiCreature(SVGMobject):
    def __init__(self, color=BLUE, **kwargs):
        super().__init__(**kwargs)
        self.set_fill(color, opacity=1)
        self.eyes = VGroup()  # 簡化表示
        
    def change_mode(self, mode):
        return self.animate
    
    def change(self, expression, target=None):
        return self.animate
    
    def make_eye_contact(self, other):
        pass
