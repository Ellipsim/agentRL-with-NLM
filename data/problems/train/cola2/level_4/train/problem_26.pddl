

(define (problem BW-rand-6)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 - block)
(:init
(handempty)
(on b1 b6)
(ontable b2)
(ontable b3)
(on b4 b3)
(on b5 b1)
(ontable b6)
(clear b2)
(clear b4)
(clear b5)
)
(:goal
(and
(on b1 b4)
(on b3 b5)
(on b4 b2)
(on b5 b6))
)
)


