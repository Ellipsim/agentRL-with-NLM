

(define (problem BW-rand-13)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 - block)
(:init
(handempty)
(on b1 b8)
(on b2 b1)
(on b3 b9)
(on b4 b12)
(ontable b5)
(ontable b6)
(on b7 b11)
(on b8 b7)
(on b9 b4)
(on b10 b5)
(on b11 b3)
(on b12 b6)
(on b13 b2)
(clear b10)
(clear b13)
)
(:goal
(and
(on b2 b1)
(on b4 b8)
(on b5 b12)
(on b6 b10)
(on b7 b2)
(on b8 b11)
(on b9 b6)
(on b10 b4)
(on b11 b3)
(on b13 b9))
)
)


