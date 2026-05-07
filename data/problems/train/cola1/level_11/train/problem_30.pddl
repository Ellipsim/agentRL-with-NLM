

(define (problem BW-rand-13)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 - block)
(:init
(handempty)
(on b1 b6)
(on b2 b10)
(on b3 b2)
(on b4 b13)
(ontable b5)
(on b6 b12)
(on b7 b9)
(on b8 b5)
(on b9 b3)
(ontable b10)
(on b11 b1)
(ontable b12)
(on b13 b11)
(clear b4)
(clear b7)
(clear b8)
)
(:goal
(and
(on b1 b11)
(on b3 b4)
(on b4 b2)
(on b5 b9)
(on b7 b12)
(on b8 b1)
(on b10 b13)
(on b13 b6))
)
)


