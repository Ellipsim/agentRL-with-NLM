

(define (problem BW-rand-14)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 b14 - block)
(:init
(handempty)
(ontable b1)
(on b2 b8)
(on b3 b5)
(on b4 b2)
(on b5 b10)
(on b6 b4)
(on b7 b11)
(on b8 b3)
(on b9 b7)
(on b10 b1)
(on b11 b13)
(on b12 b14)
(on b13 b6)
(on b14 b9)
(clear b12)
)
(:goal
(and
(on b1 b13)
(on b2 b7)
(on b3 b9)
(on b4 b6)
(on b7 b3)
(on b8 b4)
(on b9 b11)
(on b12 b5)
(on b13 b14))
)
)


