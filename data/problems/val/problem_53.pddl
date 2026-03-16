

(define (problem BW-rand-6)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 - block)
(:init
(handempty)
(ontable b1)
(ontable b2)
(ontable b3)
(on b4 b6)
(on b5 b1)
(on b6 b2)
(clear b3)
(clear b4)
(clear b5)
)
(:goal
(and
(on b1 b5)
(on b2 b1)
(on b5 b3)
(on b6 b2))
)
)


