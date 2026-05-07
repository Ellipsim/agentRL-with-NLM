

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b2)
(on b2 b4)
(ontable b3)
(on b4 b10)
(on b5 b8)
(on b6 b5)
(on b7 b6)
(on b8 b9)
(ontable b9)
(ontable b10)
(clear b1)
(clear b3)
(clear b7)
)
(:goal
(and
(on b1 b4)
(on b2 b6)
(on b7 b2)
(on b8 b1)
(on b9 b5)
(on b10 b9))
)
)


