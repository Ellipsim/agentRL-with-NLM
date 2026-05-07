

(define (problem BW-rand-6)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 - block)
(:init
(handempty)
(on b1 b2)
(ontable b2)
(ontable b3)
(ontable b4)
(on b5 b1)
(on b6 b3)
(clear b4)
(clear b5)
(clear b6)
)
(:goal
(and
(on b1 b2)
(on b2 b4)
(on b3 b1)
(on b6 b5))
)
)


