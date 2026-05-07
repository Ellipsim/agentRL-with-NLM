

(define (problem BW-rand-8)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(on b1 b8)
(on b2 b5)
(on b3 b7)
(ontable b4)
(ontable b5)
(on b6 b2)
(on b7 b1)
(on b8 b6)
(clear b3)
(clear b4)
)
(:goal
(and
(on b2 b3)
(on b3 b1)
(on b4 b7)
(on b5 b8)
(on b6 b2)
(on b7 b5))
)
)


