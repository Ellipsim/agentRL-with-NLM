

(define (problem BW-rand-13)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 - block)
(:init
(handempty)
(on b1 b9)
(on b2 b8)
(on b3 b10)
(on b4 b2)
(on b5 b7)
(on b6 b4)
(ontable b7)
(on b8 b5)
(on b9 b12)
(ontable b10)
(on b11 b6)
(on b12 b11)
(on b13 b3)
(clear b1)
(clear b13)
)
(:goal
(and
(on b1 b9)
(on b2 b10)
(on b5 b7)
(on b6 b3)
(on b8 b13)
(on b9 b5)
(on b10 b12)
(on b11 b8)
(on b12 b11)
(on b13 b6))
)
)


