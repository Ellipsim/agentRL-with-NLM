

(define (problem BW-rand-6)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 - block)
(:init
(handempty)
(on b1 b6)
(on b2 b4)
(ontable b3)
(ontable b4)
(ontable b5)
(ontable b6)
(clear b1)
(clear b2)
(clear b3)
(clear b5)
)
(:goal
(and
(on b3 b2)
(on b4 b5)
(on b5 b3))
)
)


