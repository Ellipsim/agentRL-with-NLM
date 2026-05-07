

(define (problem BW-rand-8)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(on b1 b3)
(on b2 b6)
(on b3 b8)
(ontable b4)
(on b5 b7)
(on b6 b1)
(on b7 b4)
(on b8 b5)
(clear b2)
)
(:goal
(and
(on b2 b4)
(on b3 b5)
(on b5 b1)
(on b6 b2)
(on b7 b8))
)
)


