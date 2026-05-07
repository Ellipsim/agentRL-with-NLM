

(define (problem BW-rand-6)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 - block)
(:init
(handempty)
(on b1 b3)
(ontable b2)
(on b3 b2)
(on b4 b5)
(on b5 b6)
(on b6 b1)
(clear b4)
)
(:goal
(and
(on b2 b6)
(on b3 b4)
(on b4 b2)
(on b6 b5))
)
)


