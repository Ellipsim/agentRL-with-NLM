

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(on b1 b10)
(on b2 b6)
(ontable b3)
(on b4 b11)
(ontable b5)
(ontable b6)
(on b7 b5)
(on b8 b9)
(ontable b9)
(on b10 b8)
(ontable b11)
(clear b1)
(clear b2)
(clear b3)
(clear b4)
(clear b7)
)
(:goal
(and
(on b1 b5)
(on b3 b6)
(on b4 b3)
(on b5 b10)
(on b7 b2)
(on b9 b11)
(on b10 b9)
(on b11 b4))
)
)


