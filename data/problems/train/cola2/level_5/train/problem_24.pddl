

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
(on b6 b1)
(clear b5)
(clear b6)
)
(:goal
(and
(on b1 b5)
(on b3 b1)
(on b4 b3)
(on b6 b4))
)
)


