

(define (problem BW-rand-13)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 - block)
(:init
(handempty)
(on b1 b3)
(on b2 b1)
(on b3 b10)
(ontable b4)
(ontable b5)
(on b6 b12)
(on b7 b6)
(on b8 b2)
(on b9 b7)
(on b10 b13)
(ontable b11)
(on b12 b4)
(on b13 b5)
(clear b8)
(clear b9)
(clear b11)
)
(:goal
(and
(on b1 b11)
(on b3 b2)
(on b4 b13)
(on b7 b8)
(on b8 b6)
(on b9 b12)
(on b10 b4)
(on b11 b3)
(on b12 b1))
)
)


