

(define (problem BW-rand-13)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 - block)
(:init
(handempty)
(on b1 b12)
(on b2 b1)
(on b3 b10)
(ontable b4)
(on b5 b7)
(on b6 b11)
(ontable b7)
(on b8 b9)
(on b9 b2)
(on b10 b13)
(on b11 b4)
(on b12 b5)
(on b13 b8)
(clear b3)
(clear b6)
)
(:goal
(and
(on b1 b7)
(on b2 b4)
(on b3 b1)
(on b4 b8)
(on b5 b13)
(on b6 b12)
(on b10 b9)
(on b11 b3)
(on b12 b10)
(on b13 b11))
)
)


