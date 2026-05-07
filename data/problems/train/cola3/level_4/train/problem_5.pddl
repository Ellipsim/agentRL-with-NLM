

(define (problem BW-rand-6)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 - block)
(:init
(handempty)
(on b1 b2)
(ontable b2)
(on b3 b4)
(ontable b4)
(on b5 b3)
(on b6 b5)
(clear b1)
(clear b6)
)
(:goal
(and
(on b3 b6)
(on b6 b5))
)
)


