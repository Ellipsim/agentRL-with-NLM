

(define (problem BW-rand-13)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 - block)
(:init
(handempty)
(on b1 b3)
(on b2 b12)
(on b3 b11)
(on b4 b2)
(on b5 b13)
(on b6 b7)
(ontable b7)
(ontable b8)
(on b9 b4)
(on b10 b5)
(ontable b11)
(on b12 b10)
(on b13 b1)
(clear b6)
(clear b8)
(clear b9)
)
(:goal
(and
(on b1 b11)
(on b3 b9)
(on b4 b8)
(on b6 b7)
(on b10 b3)
(on b11 b10)
(on b12 b4))
)
)


