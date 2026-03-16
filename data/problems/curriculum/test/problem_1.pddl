

(define (problem BW-rand-6)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 - block)
(:init
(handempty)
(on b1 b3)
(on b2 b5)
(on b3 b4)
(on b4 b6)
(on b5 b1)
(ontable b6)
(clear b2)
)
(:goal
(and
(on b1 b6)
(on b2 b4)
(on b5 b3)
(on b6 b2))
)
)


