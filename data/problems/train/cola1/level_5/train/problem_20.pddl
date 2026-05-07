

(define (problem BW-rand-6)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 - block)
(:init
(handempty)
(on b1 b6)
(ontable b2)
(on b3 b2)
(ontable b4)
(ontable b5)
(on b6 b5)
(clear b1)
(clear b3)
(clear b4)
)
(:goal
(and
(on b1 b2)
(on b2 b3)
(on b3 b4)
(on b4 b6)
(on b6 b5))
)
)


