

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b9)
(on b2 b8)
(ontable b3)
(on b4 b10)
(ontable b5)
(on b6 b4)
(on b7 b3)
(ontable b8)
(on b9 b6)
(ontable b10)
(clear b1)
(clear b2)
(clear b5)
(clear b7)
)
(:goal
(and
(on b4 b8)
(on b6 b9)
(on b7 b6)
(on b8 b3)
(on b9 b2))
)
)


