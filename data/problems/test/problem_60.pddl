

(define (problem BW-rand-9)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(on b1 b8)
(on b2 b4)
(on b3 b6)
(on b4 b7)
(on b5 b1)
(on b6 b9)
(on b7 b3)
(ontable b8)
(ontable b9)
(clear b2)
(clear b5)
)
(:goal
(and
(on b1 b7)
(on b3 b2)
(on b6 b9)
(on b7 b8)
(on b9 b3))
)
)


