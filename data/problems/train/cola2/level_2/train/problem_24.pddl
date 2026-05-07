

(define (problem BW-rand-4)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 - block)
(:init
(handempty)
(on b1 b3)
(ontable b2)
(on b3 b4)
(on b4 b2)
(clear b1)
)
(:goal
(and
(on b1 b3)
(on b2 b4)
(on b3 b2))
)
)


