

(define (problem BW-rand-6)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 - block)
(:init
(handempty)
(on b1 b3)
(on b2 b5)
(ontable b3)
(on b4 b2)
(ontable b5)
(on b6 b4)
(clear b1)
(clear b6)
)
(:goal
(and
(on b1 b3)
(on b2 b4)
(on b5 b2)
(on b6 b1))
)
)


