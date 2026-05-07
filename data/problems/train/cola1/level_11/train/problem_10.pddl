

(define (problem BW-rand-13)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 - block)
(:init
(handempty)
(on b1 b9)
(ontable b2)
(on b3 b12)
(ontable b4)
(on b5 b8)
(on b6 b7)
(on b7 b13)
(on b8 b2)
(on b9 b10)
(on b10 b6)
(on b11 b5)
(on b12 b11)
(on b13 b4)
(clear b1)
(clear b3)
)
(:goal
(and
(on b1 b7)
(on b2 b13)
(on b3 b12)
(on b4 b1)
(on b5 b10)
(on b6 b2)
(on b8 b3)
(on b10 b9)
(on b11 b5)
(on b13 b4))
)
)


