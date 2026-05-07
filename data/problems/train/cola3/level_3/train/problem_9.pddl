

(define (problem BW-rand-5)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 - block)
(:init
(handempty)
(on b1 b4)
(ontable b2)
(ontable b3)
(on b4 b3)
(on b5 b2)
(clear b1)
(clear b5)
)
(:goal
(and
(on b3 b5)
(on b4 b1)
(on b5 b2))
)
)


