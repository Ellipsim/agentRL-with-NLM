

(define (problem BW-rand-6)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 - block)
(:init
(handempty)
(ontable b1)
(on b2 b6)
(on b3 b1)
(on b4 b2)
(ontable b5)
(on b6 b3)
(clear b4)
(clear b5)
)
(:goal
(and
(on b1 b4)
(on b3 b6)
(on b4 b2)
(on b6 b1))
)
)


