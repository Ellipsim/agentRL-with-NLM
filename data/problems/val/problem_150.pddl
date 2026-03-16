

(define (problem BW-rand-3)
(:domain BLOCKS)
(:objects b1 b2 b3 - block)
(:init
(handempty)
(ontable b1)
(on b2 b1)
(ontable b3)
(clear b2)
(clear b3)
)
(:goal
(and
(on b1 b2))
)
)


