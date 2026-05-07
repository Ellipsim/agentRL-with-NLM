

(define (problem BW-rand-13)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 - block)
(:init
(handempty)
(ontable b1)
(on b2 b1)
(on b3 b5)
(ontable b4)
(on b5 b8)
(on b6 b13)
(ontable b7)
(on b8 b11)
(on b9 b2)
(on b10 b12)
(on b11 b4)
(on b12 b6)
(on b13 b9)
(clear b3)
(clear b7)
(clear b10)
)
(:goal
(and
(on b1 b8)
(on b2 b11)
(on b4 b12)
(on b5 b9)
(on b6 b1)
(on b9 b4)
(on b10 b5)
(on b12 b2)
(on b13 b10))
)
)


