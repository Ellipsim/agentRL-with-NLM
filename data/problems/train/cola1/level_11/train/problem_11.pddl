

(define (problem BW-rand-13)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 - block)
(:init
(handempty)
(on b1 b7)
(on b2 b10)
(on b3 b5)
(on b4 b3)
(on b5 b9)
(on b6 b11)
(ontable b7)
(on b8 b4)
(on b9 b12)
(ontable b10)
(on b11 b1)
(on b12 b6)
(on b13 b2)
(clear b8)
(clear b13)
)
(:goal
(and
(on b3 b9)
(on b5 b13)
(on b6 b4)
(on b8 b5)
(on b9 b7)
(on b10 b12)
(on b11 b10)
(on b12 b6)
(on b13 b1))
)
)


