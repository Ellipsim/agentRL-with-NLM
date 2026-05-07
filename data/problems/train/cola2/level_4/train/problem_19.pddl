

(define (problem BW-rand-6)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 - block)
(:init
(handempty)
(on b1 b4)
(ontable b2)
(ontable b3)
(on b4 b5)
(on b5 b2)
(ontable b6)
(clear b1)
(clear b3)
(clear b6)
)
(:goal
(and
(on b2 b4)
(on b4 b1)
(on b6 b5))
)
)


