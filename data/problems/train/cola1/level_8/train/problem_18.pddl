

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b6)
(ontable b2)
(on b3 b2)
(on b4 b10)
(ontable b5)
(on b6 b5)
(ontable b7)
(on b8 b3)
(on b9 b4)
(on b10 b7)
(clear b1)
(clear b8)
(clear b9)
)
(:goal
(and
(on b2 b3)
(on b3 b5)
(on b4 b8)
(on b5 b4)
(on b6 b1)
(on b7 b10)
(on b8 b7)
(on b10 b9))
)
)


