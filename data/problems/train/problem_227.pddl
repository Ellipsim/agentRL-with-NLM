

(define (problem BW-rand-13)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 - block)
(:init
(handempty)
(on b1 b9)
(ontable b2)
(on b3 b13)
(on b4 b2)
(on b5 b3)
(on b6 b1)
(ontable b7)
(on b8 b6)
(on b9 b11)
(on b10 b4)
(on b11 b12)
(on b12 b7)
(on b13 b10)
(clear b5)
(clear b8)
)
(:goal
(and
(on b1 b12)
(on b2 b4)
(on b3 b11)
(on b4 b8)
(on b8 b13)
(on b10 b6)
(on b11 b1)
(on b12 b7)
(on b13 b9))
)
)


