

(define (problem BW-rand-13)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 - block)
(:init
(handempty)
(on b1 b12)
(on b2 b7)
(on b3 b4)
(on b4 b5)
(ontable b5)
(on b6 b9)
(on b7 b8)
(on b8 b6)
(on b9 b11)
(on b10 b13)
(on b11 b1)
(on b12 b3)
(on b13 b2)
(clear b10)
)
(:goal
(and
(on b1 b4)
(on b2 b9)
(on b3 b6)
(on b5 b13)
(on b6 b11)
(on b8 b7)
(on b9 b10)
(on b10 b8)
(on b11 b5))
)
)


