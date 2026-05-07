

(define (problem BW-rand-13)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 - block)
(:init
(handempty)
(on b1 b2)
(on b2 b4)
(on b3 b1)
(ontable b4)
(on b5 b13)
(on b6 b3)
(ontable b7)
(on b8 b11)
(on b9 b5)
(on b10 b8)
(on b11 b6)
(on b12 b7)
(ontable b13)
(clear b9)
(clear b10)
(clear b12)
)
(:goal
(and
(on b2 b11)
(on b4 b6)
(on b5 b10)
(on b6 b1)
(on b7 b4)
(on b8 b3)
(on b9 b12)
(on b11 b7)
(on b13 b2))
)
)


