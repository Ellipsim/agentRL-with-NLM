

(define (problem BW-rand-13)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 - block)
(:init
(handempty)
(on b1 b8)
(on b2 b5)
(on b3 b4)
(on b4 b9)
(on b5 b3)
(on b6 b12)
(on b7 b2)
(on b8 b11)
(on b9 b10)
(ontable b10)
(on b11 b6)
(on b12 b13)
(ontable b13)
(clear b1)
(clear b7)
)
(:goal
(and
(on b2 b10)
(on b3 b5)
(on b4 b9)
(on b6 b4)
(on b7 b2)
(on b9 b11)
(on b10 b8)
(on b11 b12)
(on b13 b1))
)
)


