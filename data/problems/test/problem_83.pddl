

(define (problem BW-rand-14)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 b14 - block)
(:init
(handempty)
(on b1 b6)
(on b2 b13)
(on b3 b11)
(on b4 b8)
(on b5 b3)
(ontable b6)
(on b7 b4)
(on b8 b5)
(on b9 b12)
(ontable b10)
(on b11 b10)
(on b12 b7)
(on b13 b14)
(on b14 b1)
(clear b2)
(clear b9)
)
(:goal
(and
(on b1 b4)
(on b2 b12)
(on b4 b8)
(on b5 b2)
(on b6 b11)
(on b7 b9)
(on b9 b5)
(on b10 b14)
(on b13 b6))
)
)


