

(define (problem BW-rand-6)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 - block)
(:init
(handempty)
(on b1 b2)
(ontable b2)
(on b3 b1)
(ontable b4)
(ontable b5)
(on b6 b4)
(clear b3)
(clear b5)
(clear b6)
)
(:goal
(and
(on b5 b4)
(on b6 b1))
)
)


