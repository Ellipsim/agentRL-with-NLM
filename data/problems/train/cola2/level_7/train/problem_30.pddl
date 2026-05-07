

(define (problem BW-rand-8)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(on b1 b4)
(on b2 b7)
(on b3 b5)
(on b4 b6)
(ontable b5)
(on b6 b3)
(on b7 b8)
(on b8 b1)
(clear b2)
)
(:goal
(and
(on b2 b3)
(on b5 b1)
(on b6 b8)
(on b7 b2)
(on b8 b5))
)
)


