

(define (problem BW-rand-6)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 - block)
(:init
(handempty)
(ontable b1)
(ontable b2)
(on b3 b4)
(on b4 b5)
(on b5 b6)
(ontable b6)
(clear b1)
(clear b2)
(clear b3)
)
(:goal
(and
(on b2 b4)
(on b3 b5)
(on b4 b6)
(on b5 b2)
(on b6 b1))
)
)


