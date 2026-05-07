

(define (problem BW-rand-13)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 - block)
(:init
(handempty)
(on b1 b11)
(on b2 b4)
(on b3 b8)
(on b4 b10)
(on b5 b6)
(on b6 b1)
(on b7 b12)
(on b8 b9)
(on b9 b7)
(on b10 b13)
(on b11 b2)
(ontable b12)
(on b13 b3)
(clear b5)
)
(:goal
(and
(on b2 b13)
(on b3 b9)
(on b4 b12)
(on b5 b2)
(on b6 b1)
(on b7 b4)
(on b9 b5)
(on b10 b7)
(on b11 b10)
(on b13 b11))
)
)


