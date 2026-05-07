

(define (problem BW-rand-13)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 - block)
(:init
(handempty)
(on b1 b13)
(on b2 b11)
(on b3 b12)
(ontable b4)
(on b5 b7)
(on b6 b2)
(on b7 b4)
(on b8 b9)
(on b9 b5)
(on b10 b3)
(ontable b11)
(ontable b12)
(on b13 b8)
(clear b1)
(clear b6)
(clear b10)
)
(:goal
(and
(on b3 b5)
(on b4 b9)
(on b5 b4)
(on b6 b12)
(on b7 b1)
(on b10 b13)
(on b11 b8)
(on b12 b3)
(on b13 b2))
)
)


